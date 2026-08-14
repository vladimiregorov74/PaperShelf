from __future__ import annotations

import copy

from bs4 import BeautifulSoup
from bs4 import Tag

from papershelf.models import Article
from papershelf.parsers.base_parser import BaseParser
from papershelf.parsers.selectors import (
    METANIT_ARTICLE_SELECTORS,
    METANIT_CONTENT_SELECTORS,
    METANIT_REMOVE_SELECTORS,
)
from papershelf.services import HtmlCleaner

class MetanitParser(BaseParser):
    """
    Парсер статей metanit.com.
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
    
        return "metanit.com" in url.lower()
    
    # ------------------------------------------------------------------
    
    def __init__(self) -> None:
    
        self._cleaner = HtmlCleaner()
    
    # ------------------------------------------------------------------
    
    def parse(
        self,
        html: str,
        url: str,
    ) -> Article:
        """
        Разобрать HTML-страницу Metanit.
    
        Parameters
        ----------
        html:
            Исходный HTML страницы.
    
        url:
            URL страницы.
    
        Returns
        -------
        Article
            Разобранная статья.
        """
    
        soup = BeautifulSoup(
            html,
            "lxml",
        )
        
        article_html = self._parse_article_html(
            soup,
        )

        article_html = self._cleaner.clean(
	        article_html,
	        remove_selectors=METANIT_REMOVE_SELECTORS,
        )
    
        return Article(
            url=url,
            title=self._parse_title(soup),
            author="",
            source="Metanit",
            html=article_html,
            text="",
        )
    
    # ------------------------------------------------------------------
    
    def _parse_title(
        self,
        soup: BeautifulSoup,
    ) -> str:
        """
        Извлечь заголовок страницы.
        """
    
        title = soup.find("title")
    
        if title is None:
            return ""
    
        return title.get_text(
            " ",
            strip=True,
        )
    
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
    
            node = root.select_one(
                selector,
            )
    
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
            METANIT_ARTICLE_SELECTORS,
        )
    
    # ------------------------------------------------------------------
    
    def _parse_content_container(
        self,
        article: Tag,
    ) -> Tag | None:
        """
        Найти контейнер содержимого статьи.
        """
    
        return self._find_first(
            article,
            METANIT_CONTENT_SELECTORS,
        )
    
    # ------------------------------------------------------------------
    
    @staticmethod
    def _clone_container(
        container: Tag,
    ) -> Tag:
        """
        Создать копию HTML-контейнера.
        """
    
        return copy.deepcopy(
            container,
        )
    
    # ------------------------------------------------------------------
    
    def _parse_article_html(
        self,
        soup: BeautifulSoup,
    ) -> str:
        """
        Извлечь HTML статьи.
        """
    
        article = self._parse_article_container(
            soup,
        )
    
        if article is None:
            return ""
    
        content = self._parse_content_container(
            article,
        )
    
        if content is None:
            content = article
    
        content = self._clone_container(
            content,
        )
    
        return str(content)