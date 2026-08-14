from __future__ import annotations

from bs4 import Tag

from .container_analyzer import ContainerAnalyzer
from .models import ArticleCandidate, ContainerAnalysis, ChildInfo
from .constants import ARTICLE_MIN_CHILD_SCORE, ARTICLE_CHILD_DOMINANCE_RATIO

# ------------------------------------------------------------------


class ArticleDetector:
    """
    Поиск контейнера статьи.
    """

    # ------------------------------------------------------------------

    def __init__(
            self,
    ) -> None:
        
        self._analyzer = ContainerAnalyzer()
        self._element: Tag | None = None

    # ------------------------------------------------------------------
    
    def detect(
            self,
            root: Tag,
    ) -> ArticleCandidate:
        """
        Найти контейнер статьи.
        """
        
        return self._walk(
            element=root,
            depth=0,
            path=[],
        )
    
    # ------------------------------------------------------------------
    
    def _best_child(
            self,
            analysis: ContainerAnalysis,
    ) -> ChildInfo | None:
        """
        Найти лучшего дочернего контейнера.

        Parameters
        ----------
        analysis:
            Анализ контейнера.

        Returns
        -------
        ChildInfo | None
        """
        
        if not analysis.children:
            return None
        
        return max(
            analysis.children,
            key=lambda child: child.score,
        )
    
    # ------------------------------------------------------------------
    
    def _find_child(
            self,
            parent: Tag,
            selector: str,
    ) -> Tag | None:
        """
        Найти дочерний контейнер по CSS-селектору.

        Parameters
        ----------
        parent:
            Родительский контейнер.

        selector:
            CSS-селектор.

        Returns
        -------
        Tag | None
        """
        
        return parent.select_one(
            selector,
        )
    
    # ------------------------------------------------------------------
    
    def _walk(
            self,
            element: Tag,
            depth: int,
            path: list[str],
            named_ancestor: Tag | None = None,
    ) -> ArticleCandidate:
        """
        Выполнить поиск статьи, начиная с указанного контейнера.

        Parameters
        ----------
        element:
            Текущий HTML-контейнер.

        depth:
            Глубина обхода.

        path:
            Путь до контейнера.

        named_ancestor:
            Ближайший пройденный предок (или сам исходный элемент),
            у которого есть id или class. Нужен, чтобы в конце спуска,
            если мы остановились на безымянном <div> (просто голая
            transit-обёртка без потери контента по пути), откатиться
            к нему — селектор будет специфичнее при том же содержимом.

        Returns
        -------
        ArticleCandidate
        """
        
        if element.get("id") or element.get("class"):
            named_ancestor = element
        
        analysis = self._analyzer.analyze(
            element,
        )
        
        self._debug(
            depth,
            f"Container: {analysis.selector}",
        )
        
        current_path = [
            *path,
            analysis.selector,
        ]
        
        best_child = self._best_child(
            analysis,
        )
        
        if best_child is None:
            self._debug(
                depth,
                "No suitable child.",
            )
            return self._finalize(
                element=element,
                analysis=analysis,
                depth=depth,
                current_path=current_path,
                named_ancestor=named_ancestor,
            )
        
        self._debug(
            depth,
            (
                f"Best child: "
                f"{best_child.selector} "
                f"({best_child.score:.1f})"
            ),
        )
        
        should_descend = self._should_descend(
            element,
            analysis,
            best_child,
        )
        
        self._debug(
            depth,
            f"Should descend: {should_descend}",
        )
        
        if not should_descend:
            return self._finalize(
                element=element,
                analysis=analysis,
                depth=depth,
                current_path=current_path,
                named_ancestor=named_ancestor,
            )
        
        # Раньше здесь заново искали элемент по CSS-селектору
        # (parent.select_one(best_child.selector)) — это ненадёжно для
        # безымянных div без id/class (см. комментарий в ChildInfo.element).
        # Теперь просто берём сохранённую при анализе ссылку на сам Tag —
        # никакой неоднозначности.
        child_element = best_child.element
        
        if child_element is None:
            self._debug(
                depth,
                "Child element not found.",
            )
            return self._finalize(
                element=element,
                analysis=analysis,
                depth=depth,
                current_path=current_path,
                named_ancestor=named_ancestor,
            )
        
        return self._walk(
            element=child_element,
            depth=depth + 1,
            path=current_path,
            named_ancestor=named_ancestor,
        )
    
    # ------------------------------------------------------------------
    
    def _finalize(
            self,
            element: Tag,
            analysis: ContainerAnalysis,
            depth: int,
            current_path: list[str],
            named_ancestor: Tag | None,
    ) -> ArticleCandidate:
        """
        Завершить спуск, при необходимости откатившись к ближайшему
        именованному предку.

        Если текущая точка остановки — безымянный <div> (нет ни id,
        ни class), а по пути был предок с id/class, который держит
        почти весь тот же текст (>= 97%, то есть между ними не было
        реальной фильтрации контента — просто транзитные обёртки),
        используем этого предка: контент тот же, а селектор надёжнее.
        """
        
        if (
                named_ancestor is not None
                and named_ancestor is not element
                and not element.get("id")
                and not element.get("class")
        ):
            element_text = len(
                element.get_text(
                    strip=True,
                )
            )
            
            ancestor_text = len(
                named_ancestor.get_text(
                    strip=True,
                )
            )
            
            if (
                    ancestor_text > 0
                    and element_text / ancestor_text >= 0.97
            ):
                element = named_ancestor
                analysis = self._analyzer.analyze(
                    element,
                )
        
        self._element = element
        
        return ArticleCandidate(
            selector=analysis.selector,
            score=0.0,
            depth=depth,
            path=current_path,
            analysis=analysis,
            element=element,
        )
    
    # ------------------------------------------------------------------
    
    def _should_descend(
            self,
            element: Tag,
            current: ContainerAnalysis,
            child: ChildInfo,
    ) -> bool:
        """
        Определить, следует ли перейти к дочернему контейнеру.

        Спуск разрешён, только если ребёнок одновременно:
        1) набрал минимальный абсолютный балл (ARTICLE_MIN_CHILD_SCORE) —
           отсекает совсем пустые/незначимые элементы;
        2) содержит подавляющую долю текста ТЕКУЩЕГО контейнера
           (ARTICLE_CHILD_DOMINANCE_RATIO) — без этого условия
           абсолютный порог из пункта 1 калибруется под один масштаб
           страниц и либо не даёт спуститься на маленьких страницах,
           либо проваливается во внутренний фрагмент (например,
           единственный <ul> с парой пунктов) на больших.

        Parameters
        ----------
        element:
            Текущий HTML-элемент (для оценки его полного текста).

        current:
            Анализ текущего контейнера.

        child:
            Лучший дочерний контейнер.

        Returns
        -------
        bool
        """
        
        if child.score < ARTICLE_MIN_CHILD_SCORE:
            return False
        
        total_text = len(
            element.get_text(
                strip=True,
            )
        )
        
        if total_text == 0:
            return False
        
        dominance = child.text_length / total_text
        
        return dominance >= ARTICLE_CHILD_DOMINANCE_RATIO
    
    # ------------------------------------------------------------------
    
    def _debug(
            self,
            depth: int,
            message: str,
    ) -> None:
        """
        Вывести диагностическое сообщение.

        Parameters
        ----------
        depth:
            Текущая глубина.

        message:
            Сообщение.
        """
        
        indent = "    " * depth
        
        print(
            f"{indent}{message}",
        )
    
    # ------------------------------------------------------------------
    
    def get_element(self) -> Tag | None:
        """
        Вернуть найденный HTML-контейнер статьи.

        Returns
        -------
        Tag | None
            HTML-элемент найденного контейнера.
        """
        
        return self._element