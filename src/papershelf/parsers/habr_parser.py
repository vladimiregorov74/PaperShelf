from __future__ import annotations

from bs4 import BeautifulSoup

from papershelf.models import Article
from papershelf.parsers.base_parser import BaseParser


class HabrParser(BaseParser):
    """Парсер статей Хабра."""

    def parse(self, html: str, url: str) -> Article:

        soup = BeautifulSoup(html, "lxml")

        return Article(
            url=url,
            title=self._parse_title(soup),
            author=self._parse_author(soup),
            source="Habr",
            html=html,
            text="",
        )

    # ------------------------------------------------------------------

    def _parse_title(self, soup: BeautifulSoup) -> str:

        title = soup.find("title")

        if title is None:
            return ""

        return title.get_text(strip=True)

    # ------------------------------------------------------------------

    def _parse_author(self, soup: BeautifulSoup) -> str:

        selectors = [
            "a.tm-user-info__username",
            "span.tm-user-info__user",
            "a.author-name",
        ]

        for selector in selectors:

            node = soup.select_one(selector)

            if node:
                return node.get_text(strip=True)

        return ""