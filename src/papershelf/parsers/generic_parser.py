from __future__ import annotations

import copy
from dataclasses import dataclass
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from bs4 import Tag

from papershelf.models import Article
from papershelf.parsers.base_parser import BaseParser
from papershelf.services.html_cleaner import HtmlCleaner


# ------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class SiteConfig:
    """
    Конфигурация одного сайта: то единственное, что отличает
    MetanitParser от HabrParser — всё остальное было одинаковым
    кодом, скопированным между файлами.
    """
    
    domain: str
    source: str
    identifier: str = ""
    article_selectors: tuple[str, ...] = ()
    content_selectors: tuple[str, ...] = ()
    remove_selectors: tuple[str, ...] = ()
    author_selectors: tuple[str, ...] = ()
    title_suffix: str = ""


# ------------------------------------------------------------------


class GenericParser(BaseParser):
    """
    Универсальный парсер статей, управляемый конфигом сайта
    (SiteConfig) вместо отдельного класса на каждый сайт.

    Логика разбора HTML у всех сайтов на selectors.py одинаковая:
    найти контейнер статьи -> найти внутри него контейнер контента ->
    вычистить шум -> достать заголовок/автора. Отличается только
    набор селекторов и имя источника — они и вынесены в SiteConfig.
    """

    # ------------------------------------------------------------------

    def __init__(
        self,
        config: SiteConfig,
    ) -> None:

        self._config = config
        self._cleaner = HtmlCleaner()

    # ------------------------------------------------------------------

    def can_parse(
        self,
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

        return self._config.domain in url.lower()

    # ------------------------------------------------------------------

    def parse(
        self,
        html: str,
        url: str,
    ) -> Article:
        """
        Разобрать HTML-страницу.

        Parameters
        ----------
        html:
            Исходный HTML страницы.

        url:
            URL страницы.

        Returns
        -------
        Article
        """

        soup = BeautifulSoup(
            html,
            "lxml",
        )

        article_html = self._parse_article_html(
            soup,
            url,
        )

        article_html = self._cleaner.clean(
            article_html,
            remove_selectors=self._config.remove_selectors,
        )

        return Article(
            url=url,
            title=self._parse_title(soup),
            author=self._parse_author(soup),
            source=self._config.source,
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

        text = title.get_text(
            " ",
            strip=True,
        )

        if self._config.title_suffix and text.endswith(self._config.title_suffix):
            text = text[: -len(self._config.title_suffix)].strip()

        return text

    # ------------------------------------------------------------------

    def _parse_author(
        self,
        soup: BeautifulSoup,
    ) -> str:
        """
        Извлечь автора по первому совпавшему селектору из
        AUTHOR_SELECTORS.
        """

        for selector in self._config.author_selectors:

            node = soup.select_one(
                selector,
            )

            if node is None:
                continue

            if node.name == "meta":
                return node.get(
                    "content",
                    "",
                ).strip()

            return node.get_text(
                strip=True,
            )

        return ""

    # ------------------------------------------------------------------

    @staticmethod
    def _find_first(
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
            self._config.article_selectors,
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
            self._config.content_selectors,
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
        url: str,
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

        self._resolve_images(
            content,
            url,
        )

        return str(content)

    # ------------------------------------------------------------------

    @staticmethod
    def _resolve_images(
        content: Tag,
        base_url: str,
    ) -> None:
        """
        Привести src картинок к абсолютным URL — с учётом ленивой
        (lazy) загрузки.

        Многие сайты кладут в src крошечную заглушку (прозрачный
        gif / 1x1 base64-SVG), а настоящий адрес — в отдельном
        data-*-атрибуте (data-src, data-original, data-lazy-src,
        data-zzload-source-img и т.п. — имя отличается от сайта к
        сайту, но почти всегда содержит "src" или "source"). Без
        этого AssetDownloader получает на вход data:-заглушку,
        честно её пропускает (data: специально не скачивается) — и
        картинка просто не сохраняется, хотя реальный путь был
        прямо рядом в разметке.

        Parameters
        ----------
        content:
            HTML-контейнер статьи (уже склонированный).

        base_url:
            URL исходной страницы — база для относительных путей.
        """

        for image in content.find_all(
            "img",
        ):
            src = GenericParser._real_src(
                image,
            )

            if not src:
                continue

            image["src"] = urljoin(
                base_url,
                src,
            )

    # ------------------------------------------------------------------

    @staticmethod
    def _real_src(
        image: Tag,
    ) -> str | None:
        """
        Найти реальный URL картинки среди атрибутов тега.

        Приоритет: любой атрибут (кроме самого src и *srcset — у
        него другой, многозначный формат "url 1x, url 2x"), чьё имя
        содержит "src" или "source" и чьё значение не выглядит
        data:-заглушкой. Если такого нет — используется обычный src.
        """

        for attr_name, attr_value in image.attrs.items():

            if attr_name == "src":
                continue

            if not isinstance(attr_value, str):
                continue

            lowered = attr_name.lower()

            if "srcset" in lowered:
                continue

            if "src" not in lowered and "source" not in lowered:
                continue

            if not attr_value or attr_value.startswith("data:"):
                continue

            return attr_value

        return image.get(
            "src",
        )

    # ------------------------------------------------------------------
    
    @property
    def config(self) -> SiteConfig:
        return self._config