from __future__ import annotations

from bs4 import BeautifulSoup
from bs4 import Tag


class HtmlCleaner:
    """
    Выполняет очистку HTML статьи.

    Класс не зависит от конкретного сайта и может
    использоваться любым парсером.
    """

    _REMOVE_SELECTORS = (
        "script",
        "style",
        "noscript",
        ".code-explainer",
    )

    # ------------------------------------------------------------------

    def clean(
        self,
        html: str,
    ) -> str:
        """
        Очистить HTML.
        """

        soup = BeautifulSoup(html, "lxml")

        self._remove_elements(soup)

        return str(soup)

    # ------------------------------------------------------------------

    def _remove_elements(
        self,
        root: BeautifulSoup | Tag,
    ) -> None:
        """
        Удалить ненужные элементы.
        """

        for selector in self._REMOVE_SELECTORS:

            for node in root.select(selector):
                node.decompose()