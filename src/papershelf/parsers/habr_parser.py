from __future__ import annotations

import copy

from bs4 import BeautifulSoup
from bs4 import Tag

from papershelf.models import Article
from papershelf.parsers.base_parser import BaseParser
from papershelf.parsers.selectors import (
    HABR_ARTICLE_SELECTORS,
    HABR_AUTHOR_SELECTORS,
    HABR_CONTENT_SELECTORS,
)
from papershelf.services import HtmlCleaner


class HabrParser(BaseParser):
    """
    Парсер статей Habr.
    """
    # ------------------------------------------------------------------

    @classmethod
    def can_parse(
        cls,
        url: str,
    ) -> bool:
        """
        Проверить поддержку URL.

        Parameters
        ----------
        url:
            Адрес страницы.

        Returns
        -------
        bool
        """

        return "habr.com" in url.lower()

    
    # ------------------------------------------------------------------

    def __init__(self) -> None:

        self._cleaner = HtmlCleaner()

    # ------------------------------------------------------------------

    def parse(
        self,
        html: str,
        url: str,
    ) -> Article:

        soup = BeautifulSoup(html, "lxml")

        article_html = self._parse_article_html(soup)

        article_html = self._cleaner.clean(article_html)

        return Article(
            url=url,
            title=self._parse_title(soup),
            author=self._parse_author(soup),
            source="Habr",
            html=article_html,
            text="",
        )

    # ------------------------------------------------------------------

    def _parse_title(
        self,
        soup: BeautifulSoup,
    ) -> str:

        title = soup.find("title")

        if title is None:
            return ""

        return (
            title.get_text(" ", strip=True)
            .replace(" / Хабр", "")
            .strip()
        )

    # ------------------------------------------------------------------

    def _parse_author(
        self,
        soup: BeautifulSoup,
    ) -> str:

        for selector in HABR_AUTHOR_SELECTORS:

            node = soup.select_one(selector)

            if node is None:
                continue

            if node.name == "meta":
                return node.get("content", "").strip()

            return node.get_text(strip=True)

        return ""

    # ------------------------------------------------------------------

    def _find_first(
        self,
        root: BeautifulSoup | Tag,
        selectors: tuple[str, ...],
    ) -> Tag | None:

        for selector in selectors:

            node = root.select_one(selector)

            if node is not None:
                return node

        return None

    # ------------------------------------------------------------------

    def _parse_article_container(
        self,
        soup: BeautifulSoup,
    ) -> Tag | None:

        return self._find_first(
            soup,
            HABR_ARTICLE_SELECTORS,
        )

    # ------------------------------------------------------------------

    def _parse_content_container(
        self,
        article: Tag,
    ) -> Tag | None:

        return self._find_first(
            article,
            HABR_CONTENT_SELECTORS,
        )

    # ------------------------------------------------------------------

    def _clone_container(
        self,
        container: Tag,
    ) -> Tag:

        return copy.deepcopy(container)

    # ------------------------------------------------------------------

    def _parse_article_html(
        self,
        soup: BeautifulSoup,
    ) -> str:

        article = self._parse_article_container(soup)

        if article is None:
            return ""

        content = self._parse_content_container(article)

        if content is None:
            content = article

        content = self._clone_container(content)

        return str(content)