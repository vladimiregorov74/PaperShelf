from __future__ import annotations

from bs4 import BeautifulSoup
from bs4 import Tag

from papershelf.models import Article
from papershelf.parsers.base_parser import BaseParser


class HabrParser(BaseParser):
    """
    Парсер статей Habr.
    """

    def parse(
        self,
        html: str,
        url: str,
    ) -> Article:

        soup = BeautifulSoup(html, "lxml")

        return Article(
            url=url,
            title=self._parse_title(soup),
            author=self._parse_author(soup),
            source="Habr",
            html=self._parse_article_html(soup),
            text="",
        )

    # ---------------------------------------------------------

    def _parse_title(
        self,
        soup: BeautifulSoup,
    ) -> str:

        title = soup.find("title")

        if title is None:
            return ""

        return (
            title
            .get_text(" ", strip=True)
            .replace(" / Хабр", "")
            .strip()
        )

    # ---------------------------------------------------------

    def _parse_author(
        self,
        soup: BeautifulSoup,
    ) -> str:

        selectors = (
            "a.tm-user-info__username",
            "span.tm-user-info__username",
            "a[class*='user-info']",
            "meta[name='author']",
        )

        for selector in selectors:

            node = soup.select_one(selector)

            if node is None:
                continue

            if node.name == "meta":
                return node.get("content", "").strip()

            return node.get_text(strip=True)

        return ""

    # ---------------------------------------------------------

    def _parse_article_container(
        self,
        soup: BeautifulSoup,
    ) -> Tag | None:

        selectors = (
            "article.tm-article-presenter__content",
            "div.tm-article-body",
            "article",
            "main article",
        )

        for selector in selectors:

            node = soup.select_one(selector)

            if node is not None:
                return node

        return None

    # ---------------------------------------------------------

    def _parse_article_html(
        self,
        soup: BeautifulSoup,
    ) -> str:

        container = self._parse_article_container(soup)

        if container is None:
            return ""

        return str(container)