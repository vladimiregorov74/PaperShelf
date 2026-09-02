from __future__ import annotations

from bs4 import BeautifulSoup
from bs4 import Tag

from papershelf.config.constants import REMOVE_SELECTORS


class HtmlCleaner:
    """
    Выполняет очистку HTML статьи.

    Класс не зависит от конкретного сайта и может
    использоваться любым парсером.
    """

    _REMOVE_SELECTORS = REMOVE_SELECTORS

    # ------------------------------------------------------------------

    def clean(
        self,
        html: str,
        remove_selectors: tuple[str, ...] = (),
    ) -> str:
        """
        Очистить HTML статьи.

        Parameters
        ----------
        html:
            HTML-код статьи.

        remove_selectors:
            Дополнительные CSS-селекторы элементов,
            которые необходимо удалить для конкретного сайта.

        Returns
        -------
        str
            Очищенный HTML.
        """

        soup = BeautifulSoup(
            html,
            "lxml",
        )

        self._remove_elements(
            soup,
            remove_selectors,
        )

        self._normalize_figures(
            soup,
        )

        body = soup.body

        if body is None:
            result = str(soup)
        else:
            result = "".join(
                str(child)
                for child in body.children
            )

        result = result.replace(
            ' xmlns="http://www.w3.org/1999/xhtml"',
            "",
        )

        return result

    # ------------------------------------------------------------------

    def _remove_elements(
        self,
        root: BeautifulSoup | Tag,
        remove_selectors: tuple[str, ...],
    ) -> None:
        """
        Удалить ненужные элементы.

        Сначала применяются общие правила очистки,
        затем правила конкретного сайта.
        """

        selectors = (
            self._REMOVE_SELECTORS
            + remove_selectors
        )

        for selector in selectors:

            for node in root.select(
                selector,
            ):
                node.decompose()

    # ------------------------------------------------------------------

    def _normalize_figures(
        self,
        root: BeautifulSoup | Tag,
    ) -> None:
        """
        Заменить <figure> на обычный <div>.

        QTextBrowser некорректно отображает figure,
        поэтому используем обычный блочный контейнер.
        """

        for figure in root.find_all(
            "figure",
        ):

            wrapper = root.new_tag(
                "div",
            )

            wrapper["class"] = "figure"

            for child in list(
                figure.children,
            ):
                wrapper.append(
                    child.extract(),
                )

            figure.replace_with(
                wrapper,
            )