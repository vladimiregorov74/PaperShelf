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


class HabrParser(BaseParser):
    """
    Парсер статей Habr.
    """

    # ------------------------------------------------------------------

    def parse(
        self,
        html: str,
        url: str,
    ) -> Article:
        """
        Преобразовать HTML страницы в объект Article.
        """

        soup = BeautifulSoup(html, "lxml")

        return Article(
            url=url,
            title=self._parse_title(soup),
            author=self._parse_author(soup),
            source="Habr",
            html=self._parse_article_html(soup),
            text="",
        )

    # ------------------------------------------------------------------

    def _parse_title(
        self,
        soup: BeautifulSoup,
    ) -> str:
        """
        Получить заголовок статьи.
        """

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
        """
        Получить автора статьи.
        """

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
        """
        Найти первый элемент по списку CSS-селекторов.
        """

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
        """
        Найти контейнер статьи.
        """

        return self._find_first(
            soup,
            HABR_ARTICLE_SELECTORS,
        )

    # ------------------------------------------------------------------

    def _parse_content_container(
        self,
        article: Tag,
    ) -> Tag | None:
        """
        Найти контейнер с содержимым статьи.
        """

        return self._find_first(
            article,
            HABR_CONTENT_SELECTORS,
        )

    # ------------------------------------------------------------------

    def _clone_container(
        self,
        container: Tag,
    ) -> Tag:
        """
        Создать независимую копию контейнера.
        """

        return copy.deepcopy(container)

    # ------------------------------------------------------------------

    def _remove_unwanted_elements(
        self,
        container: Tag,
    ) -> None:
        """
        Удалить элементы,
        которые не нужны в сохраненной статье.
        """

        selectors = (
            "script",
            "style",
            "noscript",
        )

        for selector in selectors:

            for node in container.select(selector):
                node.decompose()

    # ------------------------------------------------------------------

    def _parse_article_html(
        self,
        soup: BeautifulSoup,
    ) -> str:
        """
        Получить HTML статьи.
        """

        article = self._parse_article_container(soup)

        if article is None:
            return ""

        content = self._parse_content_container(article)

        if content is None:
            content = article

        content = self._clone_container(content)

        self._remove_unwanted_elements(content)

        return str(content)