from __future__ import annotations

import re

import soupsieve
from bs4 import Tag

from .models import CleaningReport

# ------------------------------------------------------------------

# Голый селектор без класса/id/атрибута (например просто "p" или "div")
# слишком неспецифичен для удаления: он совпадёт с КАЖДЫМ элементом
# этого тега во всём поддереве, а не с тем ОДНИМ конкретным элементом,
# для которого изначально считался score. Такие решения возникают у
# CleaningDecision с reason="zero score" — когда у забракованного
# элемента просто не было своего class/id, и ChildInfo.selector
# выродился в голое имя тега. SelectorGenerator уже отфильтровывает
# reason="zero score" при записи в selectors.py (поэтому боевой
# HtmlCleaner не страдает), но этот класс — собственный live-предпросмотр
# инструмента — раньше применял ВЕСЬ report.remove без такого фильтра.
# После починки soupsieve.match() (см. _remove) это стало реально
# опасно: голое "p" реально удаляет все <p> в статье. Проверяем это
# здесь, а не полагаемся на фильтр в другом файле — так безопасно
# независимо от того, кто и почему сгенерировал неспецифичный селектор.

_BARE_TAG_SELECTOR = re.compile(r"^[a-zA-Z][a-zA-Z0-9]*$")


class ArticleCleaner:
    """
    Очищает HTML-контейнер статьи от служебных элементов.

    Класс отвечает только за физическое удаление элементов.
    Решения о том, что удалить, принимает
    ArticleCleanerAnalyzer.
    """

    # ------------------------------------------------------------------

    def clean(
        self,
        element: Tag,
        report: CleaningReport,
    ) -> Tag:
        """
        Очистить HTML-контейнер согласно отчёту.

        Parameters
        ----------
        element:
            Корневой HTML-контейнер.

        report:
            Отчёт анализатора очистки.

        Returns
        -------
        Tag
            Очищенный HTML-контейнер.
        """

        selectors = {
            decision.selector
            for decision in report.remove
        }

        for selector in selectors:

            if _BARE_TAG_SELECTOR.match(
                selector,
            ):
                print(
                    "SKIP (неспецифичный селектор, "
                    "удалил бы все теги этого имени):",
                    selector,
                )
                continue

            self._remove(
                element,
                selector,
            )

        return element

    # ------------------------------------------------------------------

    @staticmethod
    def _remove(
        element: Tag,
        selector: str,
    ) -> None:
        """
        Удалить элементы, совпадающие с CSS-селектором, рекурсивно
        по всему поддереву (а не только среди прямых детей — так же,
        как это делает боевой HtmlCleaner в papershelf/services, и
        как нужно для рекламных слотов, которые обычно лежат на
        2+ уровня глубже прямых детей контейнера статьи).

        Раньше здесь было `child.select_one(selector) is child`,
        что НИКОГДА не выполняется: select_one() ищет только среди
        ПОТОМКОВ тега, не включая сам тег — то есть удаление не
        работало вообще, независимо от глубины. soupsieve.match()
        проверяет совпадение самого тега с селектором напрямую.

        Parameters
        ----------
        element:
            Корневой HTML-контейнер.

        selector:
            CSS-селектор удаляемых элементов.
        """

        for child in list(
            element.find_all(
                True,
            )
        ):
            if child.decomposed:
                # Уже удалён как потомок другого совпавшего элемента
                # на предыдущей итерации этого же списка.
                continue

            if soupsieve.match(
                selector,
                child,
            ):
                print(
                    "REMOVE:",
                    child.name,
                    child.get("id", ""),
                    child.get("class", []),
                    "images=",
                    len(child.find_all("img")),
                )
                child.decompose()