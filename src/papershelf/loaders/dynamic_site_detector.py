from __future__ import annotations

from bs4 import BeautifulSoup


class DynamicSiteDetector:
    """
    Определяет, является ли страница
    динамически загружаемой.
    """

    # ------------------------------------------------------------------

    def is_dynamic(
        self,
        html: str,
    ) -> bool:
        """
        Проверить страницу.
        """

        html_lower = html.lower()

        if self._contains_framework_markers(
            html_lower,
        ):
            return True

        soup = BeautifulSoup(
            html,
            "lxml",
        )

        return self._looks_like_spa(
            soup,
        )

    # ------------------------------------------------------------------

    def _contains_framework_markers(
        self,
        html: str,
    ) -> bool:
        """
        Проверить известные признаки SPA.
        """

        markers = (

            "__next",

            "__nuxt",

            "__remix",

            "__vite",

            "data-reactroot",

            "webpack",

            "react",

            "notion",

        )

        return any(
            marker in html
            for marker in markers
        )

    # ------------------------------------------------------------------

    def _looks_like_spa(
        self,
        soup: BeautifulSoup,
    ) -> bool:
        """
        Проверить страницу по эвристике.
        """

        text = soup.get_text(
            " ",
            strip=True,
        )

        paragraphs = soup.find_all(
            "p",
        )

        articles = soup.find_all(
            "article",
        )

        mains = soup.find_all(
            "main",
        )

        scripts = soup.find_all(
            "script",
        )

        return (

            len(text) < 300

            and len(paragraphs) == 0

            and len(articles) == 0

            and len(mains) == 0

            and len(scripts) > 10

        )