from __future__ import annotations

from bs4 import Tag

from .container_analyzer import ContainerAnalyzer
from .models import ArticleCandidate, ContainerAnalysis, ChildInfo
from .constants import ARTICLE_MIN_CHILD_SCORE

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

        Returns
        -------
        ArticleCandidate
        """
        
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
            
            return ArticleCandidate(
                selector=analysis.selector,
                score=0.0,
                depth=depth,
                path=current_path,
                analysis=analysis,
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
            analysis,
            best_child,
        )
        
        self._debug(
            depth,
            f"Should descend: {should_descend}",
        )
        
        if not should_descend:
            return ArticleCandidate(
                selector=analysis.selector,
                score=0.0,
                depth=depth,
                path=current_path,
                analysis=analysis,
            )
        
        child_element = self._find_child(
            element,
            best_child.selector,
        )
        
        if child_element is None:
            self._debug(
                depth,
                "Child element not found.",
            )
            
            return ArticleCandidate(
                selector=analysis.selector,
                score=0.0,
                depth=depth,
                path=current_path,
                analysis=analysis,
            )
        
        return self._walk(
            element=child_element,
            depth=depth + 1,
            path=current_path,
        )
    
    # ------------------------------------------------------------------
    
    def _should_descend(
            self,
            current: ContainerAnalysis,
            child: ChildInfo,
    ) -> bool:
        """
        Определить, следует ли перейти к дочернему контейнеру.

        Parameters
        ----------
        current:
            Анализ текущего контейнера.

        child:
            Лучший дочерний контейнер.

        Returns
        -------
        bool
        """
        
        return (
                child.score >= ARTICLE_MIN_CHILD_SCORE
        )
    
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