from __future__ import annotations

from bs4 import BeautifulSoup, Tag
import requests
from urllib.parse import urlparse
from pathlib import PurePosixPath

from papershelf.core.exceptions import DynamicSiteError, EmptyPageError
from .models import InspectionReport, PageInfo, HeadingInfo, ImageInfo, CodeBlockInfo, TableInfo, LinkInfo, \
    StatisticsInfo, ContainerInfo
from .constants import LANGUAGE_ALIASES, POSITIVE_CLASSES, NEGATIVE_CLASSES, LINK_WEIGHT, TABLE_WEIGHT, CODE_WEIGHT, \
    IMAGE_WEIGHT, HEADING_WEIGHT, PARAGRAPH_WEIGHT, TEXT_WEIGHT, LANGUAGE_PREFIXES, MIN_CONTAINER_TEXT
from .container_analyzer import ContainerAnalyzer
from .article_detector import ArticleDetector
from .article_cleaner_analyzer import ArticleCleanerAnalyzer
from .article_cleaner import ArticleCleaner
from .article_resource_resolver import ArticleResourceResolver
from .article_author_detector import ArticleAuthorDetector
from .selector_generator import SelectorGenerator
from .site_registry_generator import SiteRegistryGenerator
from .css_utils import build_selector
# from papershelf.loaders.smart_loader import SmartLoader

class SiteInspector:
    """
    Анализатор HTML-документов.

    Класс отвечает только за анализ страницы и
    формирование InspectionReport.
    """
    
    # ------------------------------------------------------------------

    def __init__(self) -> None:

        self._url: str = ""

        self._html: str = ""

        self._soup: BeautifulSoup | None = None

        # self._loader = SmartLoader()

        self._container_analyzer = ContainerAnalyzer()
        
        self._article_detector = ArticleDetector()
        
        self._article_cleaner_analyzer = (ArticleCleanerAnalyzer())
        
        self._article_cleaner = ArticleCleaner()
        
        self._article_resource_resolver = ArticleResourceResolver()
        
        self._article_author_detector = ArticleAuthorDetector()
        
        self._selector_generator = SelectorGenerator()
        
        self._site_registry_generator = SiteRegistryGenerator()
        
        # Прямые ссылки на Tag для контейнеров, собранных в
        # _collect_containers, ключ — id(info). Без этого
        # _find_container вынужден пересобирать CSS-селектор из
        # ContainerInfo и заново искать его через soup.select_one() —
        # а для контейнера без class/id (обычное дело — просто
        # структурная обёртка) селектор вырождается в голое имя тега
        # ("div"), и select_one находит ПЕРВЫЙ такой тег во всём
        # документе, а не тот конкретный, что был оценён скорингом.
        # Именно так на Notion контейнер с реальным контентом
        # (div.notion-page-content, score 50.74) подменялся случайной
        # обёрткой div.main в другом месте дерева.
        self._container_elements: dict[int, Tag] = {}


    # ------------------------------------------------------------------

    # def load(self, url: str, ) -> None:
    #     """
    #     Загрузить страницу.
    #
    #     Parameters
    #     ----------
    #     url:
    #         Адрес страницы.
    #     """
    #     page = self._loader.load(url)
    #
    #     self.load_html(
    #         page.html,
    #         page.url,
    #     )

    # ------------------------------------------------------------------
    
    def load_html(
            self,
            html: str,
            url: str,
    ) -> None:
        """
        Загрузить уже готовый HTML.

        Parameters
        ----------
        html:
            HTML-код страницы.

        url:
            Исходный адрес.
        """
        
        self._url = url
        
        self._html = html
        
        self._soup = BeautifulSoup(
            html,
            "lxml",
        )
        
    # ------------------------------------------------------------------
    
    def inspect(
            self,
            source: str | None = None,
            title_suffix: str = "",
    ) -> InspectionReport:
        """
        Выполнить полный анализ страницы.

        Parameters
        ----------
        source:
            Отображаемое имя источника для site_registry_data.py.
            Если не передано — подбирается автоматически по домену
            (guess_source_name); детектор не может достоверно угадать
            желаемый брендинг сайта, поэтому при необходимости
            передавайте явно (--source в inspect_site.py).

        title_suffix:
            Суффикс, отрезаемый от <title> страницы (например
            " / Хабр"). Детектор НЕ может определить его сам — это
            вопрос брендинга конкретного сайта, а не структуры DOM.
            По умолчанию пустой (--title-suffix в inspect_site.py).
        """
        
        page = self._collect_page_info()
        
        headings = self._collect_headings()
        
        images = self._collect_images()
        
        code_blocks = self._collect_code_blocks()
        
        tables = self._collect_tables()
        
        links = self._collect_links()
        
        containers = self._collect_containers()
        print(f"In inspector.inspect {source=}, {containers=}")
        
        article_candidate = None
        cleaning_report = None
        author_selectors: list[str] = []
        
        if containers:
            
            element = self._find_container(
                containers[0],
            )
            
            if element:
                article_candidate = (
                    self._article_detector.detect(
                        element,
                    )
                )
                
                cleaning_report = (
                    self._article_cleaner_analyzer.analyze(
                        article_candidate.analysis,
                        article_candidate.element,
                    )
                )
                
                author_selectors = (
                    self._article_author_detector.detect(
                        self._soup,
                    )
                )
                
                self._article_cleaner.clean(
                    article_candidate.element,
                    cleaning_report,
                )
                self._article_resource_resolver.resolve(
                    article_candidate.element,
                    self._url,
                )
                print("SITE NAME =", urlparse(self._url).netloc)
                print()
                print("=== RESOLVED IMAGES ===")
                
                for image in article_candidate.element.find_all(
                        "img",
                ):
                    print(
                        image.get("src"),
                    )
                
                print("=======================")
                print()
        
        statistics = self._create_statistics(
            headings=headings,
            images=images,
            code_blocks=code_blocks,
            tables=tables,
            links=links,
            containers=containers,
        )
        
        return InspectionReport(
            page=page,
            statistics=statistics,
            headings=headings,
            images=images,
            code_blocks=code_blocks,
            tables=tables,
            links=links,
            containers=containers,
            article_candidate=article_candidate,
            cleaning_report=cleaning_report,
            author_selectors=author_selectors,
        )

    # ------------------------------------------------------------------

    def _require_soup(
        self,
    ) -> BeautifulSoup:
        """
        Вернуть загруженный DOM.

        Raises
        ------
        RuntimeError
            Если страница ещё не загружена.
        """

        if self._soup is None:
            raise RuntimeError(
                "Страница не загружена."
            )

        return self._soup

    # ------------------------------------------------------------------

    def _collect_page_info(
        self,
    ) -> PageInfo:
        """
        Собрать общую информацию о странице.
        """

        soup = self._require_soup()

        title = ""

        if soup.title is not None:
            title = soup.title.get_text(
                strip=True,
            )

        return PageInfo(
            url=self._url,
            title=title,
        )

    # ------------------------------------------------------------------
    
    def _collect_headings(self, ) -> list[HeadingInfo]:
        """
        Собрать заголовки страницы.

        Returns
        -------
        list[HeadingInfo]
        """
        
        soup = self._require_soup()
        
        headings: list[HeadingInfo] = []
        
        for level in (
                "h1",
                "h2",
                "h3",
                "h4",
                "h5",
                "h6",
        ):
            for tag in soup.find_all(level):
                
                text = tag.get_text(
                    " ",
                    strip=True,
                )
                
                if not text:
                    continue

                headings.append(
                    HeadingInfo(
                        level=int(level[1]),
                        text=text,
                        selector=self._selector(tag),
                    )
                )
        
        return headings

    # ------------------------------------------------------------------

    def _collect_images(self, ) -> list[ImageInfo]:
        """
        Собрать изображения страницы.

        Returns
        -------
        list[ImageInfo]
        """

        soup = self._require_soup()

        images: list[ImageInfo] = []

        for tag in soup.find_all("img"):
            src = tag.get(
                "src",
                "",
            )

            images.append(
                ImageInfo(
                    src=src,
                    alt=tag.get(
                        "alt",
                        "",
                    ),
                    extension=self._extension(
                        src,
                    ),
                )
            )

        return images

    # ------------------------------------------------------------------# ------------------------------------------------------------------
    
    def _collect_code_blocks(self, ) -> list[CodeBlockInfo]:
        """
        Собрать блоки исходного кода.

        Returns
        -------
        list[CodeBlockInfo]
        """
        
        soup = self._require_soup()
        
        blocks: list[CodeBlockInfo] = []
        
        selectors = (
            "pre",
            "code",
        )
        
        for selector in selectors:
            
            for element in soup.find_all(selector):
                
                text = element.get_text(
                    "\n",
                    strip=True,
                )
                
                if not text:
                    continue
                
                classes = element.get(
                    "class",
                    [],
                )
                
                language = self._detect_language(
                    classes,
                )
                
                blocks.append(
                    CodeBlockInfo(
                        tag=element.name,
                        language=language,
                        classes=classes,
                        lines=len(text.splitlines()),
                        text=text,
                    )
                )
        
        return blocks

    # ------------------------------------------------------------------ # ------------------------------------------------------------------
    
    def _collect_tables(self, ) -> list[TableInfo]:
        """
        Собрать HTML-таблицы страницы.

        Returns
        -------
        list[TableInfo]
        """
        
        soup = self._require_soup()
        
        tables: list[TableInfo] = []
        
        for table in soup.find_all("table"):
            
            rows = table.find_all("tr")
            
            row_count = len(rows)
            
            column_count = 0
            
            for row in rows:
                cells = row.find_all(
                    [
                        "td",
                        "th",
                    ]
                )
                
                column_count = max(
                    column_count,
                    len(cells),
                )
            
            tables.append(
                TableInfo(
                    rows=row_count,
                    columns=column_count,
                    css_classes=table.get(
                        "class",
                        [],
                    ),
                )
            )
        
        return tables
    
    # ------------------------------------------------------------------
    
    def _collect_links(self, ) -> list[LinkInfo]:
        """
        Собрать ссылки страницы.

        Returns
        -------
        list[LinkInfo]
        """
        
        soup = self._require_soup()
        
        links: list[LinkInfo] = []
        
        current_host = urlparse(
            self._url,
        ).netloc
        
        for tag in soup.find_all("a"):
            
            href = tag.get(
                "href",
                "",
            ).strip()
            
            if not href:
                continue
            
            text = tag.get_text(
                " ",
                strip=True,
            )
            
            parsed = urlparse(href)
            
            if parsed.netloc:
                external = parsed.netloc != current_host
            else:
                external = False
            
            links.append(
                LinkInfo(
                    href=href,
                    text=text,
                    external=external,
                )
            )
        
        return links
    
    # ------------------------------------------------------------------
    
    def _collect_containers(
            self,
    ) -> list[ContainerInfo]:
        """
        Собрать информацию о контейнерах страницы.

        Returns
        -------
        list[ContainerInfo]
        """
        
        soup = self._require_soup()
        
        containers: list[ContainerInfo] = []
        
        for element in soup.find_all(
                [
                    "article",
                    "main",
                    "section",
                    "div",
                ]
        ):
            
            text = element.get_text(
                " ",
                strip=True,
            )
            if len(text) < MIN_CONTAINER_TEXT:
                continue
                
            if not text:
                continue
            
            info = ContainerInfo(
                tag=element.name,
                
                css_id=element.get(
                    "id",
                    "",
                ),
                
                css_classes=element.get(
                    "class",
                    [],
                ),
                
                text_length=len(text),
                
                paragraphs=len(
                    element.find_all("p")
                ),
                
                headings=len(
                    element.find_all(
                        [
                            "h1",
                            "h2",
                            "h3",
                            "h4",
                            "h5",
                            "h6",
                        ]
                    )
                ),
                
                images=len(
                    element.find_all("img")
                ),
                
                code_blocks=len(
                    element.find_all(
                        [
                            "pre",
                            "code",
                        ]
                    )
                ),
                
                tables=len(
                    element.find_all("table")
                ),
                
                links=len(
                    element.find_all("a")
                ),
            )
            
            info.score = self._score_container(
                info,
            )
            
            self._container_elements[id(info)] = element
            
            containers.append(
                info,
            )
        
        containers.sort(
            key=lambda item: item.score,
            reverse=True,
        )
        
        return containers

    # ------------------------------------------------------------------
    
    def _create_statistics(
            self,
            headings: list[HeadingInfo],
            images: list[ImageInfo],
            code_blocks: list[CodeBlockInfo],
            tables: list[TableInfo],
            links: list[LinkInfo],
            containers: list[ContainerInfo],
    ) -> StatisticsInfo:
        """
        Построить статистику страницы.

        Parameters
        ----------
        headings:
            Найденные заголовки.

        images:
            Найденные изображения.

        code_blocks:
            Найденные блоки кода.

        tables:
            Найденные таблицы.

        links:
            Найденные ссылки.

        containers:
            Найденные контейнеры.

        Returns
        -------
        StatisticsInfo
        """
        
        return StatisticsInfo(
            headings=len(headings),
            images=len(images),
            code_blocks=len(code_blocks),
            tables=len(tables),
            links=len(links),
            containers=len(containers),
        )
    
    # ------------------------------------------------------------------
    
    @staticmethod
    def _extension(path: str) -> str:
        """
        Получить расширение файла.

        Parameters
        ----------
        path:
            URL изображения.

        Returns
        -------
        str
        """
        
        parsed = urlparse(path)
        
        suffix = PurePosixPath(
            parsed.path,
        ).suffix
        
        return suffix.removeprefix(".").lower()
    
    # ------------------------------------------------------------------
    
    @classmethod
    def _detect_language(
            cls,
            classes: list[str],
    ) -> str:
        """
        Определить язык программирования по CSS-классам.

        Parameters
        ----------
        classes:
            CSS-классы элемента.

        Returns
        -------
        str
            Название языка или пустая строка.
        """
        
        for css_class in classes:
            
            css_class = css_class.lower()
            
            # Точное совпадение
            language = LANGUAGE_ALIASES.get(css_class)
            
            if language:
                return language
            
            # Поиск по известным префиксам
            for prefix in LANGUAGE_PREFIXES:
                
                if not css_class.startswith(prefix):
                    continue
                
                language = css_class.removeprefix(prefix)
                
                language = language.rstrip(";")
                
                return LANGUAGE_ALIASES.get(
                    language,
                    language,
                )
        
        return ""
    
    # ------------------------------------------------------------------
    
    def _score_container(
            self,
            container: ContainerInfo,
    ) -> float:
        """
        Рассчитать рейтинг контейнера.
        """
        
        score = 0.0
        
        # Текст
        score += container.text_length * TEXT_WEIGHT
        score += container.paragraphs * PARAGRAPH_WEIGHT
        score += container.headings * HEADING_WEIGHT
        
        # Контент
        score += container.images * IMAGE_WEIGHT
        score += container.code_blocks * CODE_WEIGHT
        score += container.tables * TABLE_WEIGHT
        
        # Штраф за ссылки
        score += container.links * LINK_WEIGHT
        
        # CSS-классы
        score += self._class_score(
            container.css_classes,
        )
        
        return score
    
    # ------------------------------------------------------------------
    @staticmethod
    def _class_score(
            classes: list[str],
    ) -> float:
        """
        Рассчитать вклад CSS-классов в рейтинг.
        """
        
        score = 0.0
        
        for css_class in classes:
            css_class = css_class.lower()
            
            score += POSITIVE_CLASSES.get(
                css_class,
                0,
            )
            
            score += NEGATIVE_CLASSES.get(
                css_class,
                0,
            )
        
        return score

    # ------------------------------------------------------------------

    def _find_container(
            self,
            info: ContainerInfo,
    ) -> Tag | None:
        """
        Вернуть Tag, сохранённый для этого контейнера в
        _collect_containers — напрямую, без пересборки CSS-селектора
        и повторного поиска (см. комментарий у self._container_elements
        в __init__ о том, почему повторный поиск ненадёжен).

        Parameters
        ----------
        info:
            Информация о контейнере.

        Returns
        -------
        Tag | None
        """

        element = self._container_elements.get(
            id(info),
        )

        if isinstance(
                element,
                Tag,
        ):
            return element

        return None

    # ------------------------------------------------------------------

    def _build_selector(
            self,
            info: ContainerInfo,
    ) -> str:
        """
        Построить CSS-селектор контейнера.

        Parameters
        ----------
        info:
            Информация о контейнере.

        Returns
        -------
        str
        """

        selector = info.tag

        if info.css_id:
            selector += f"#{info.css_id}"

        if info.css_classes:
            selector += "".join(
                f".{css_class}"
                for css_class in info.css_classes
            )

        return selector

    # ------------------------------------------------------------------

    def _selector(
            self,
            element: Tag,
    ) -> str:
        """
        Построить CSS-селектор элемента.
        """

        return build_selector(
            element,
        )
    
    from papershelf.core.exceptions import DynamicSiteError
    
  
    
    # ------------------------------------------------------------------
    
    def _check_empty_page(
            self,
    ) -> None:
        """
        Проверить, что страница содержит
        корректный HTML.
        """
        
        #
        # Пустой HTML.
        #
        
        if not self._html.strip():
            raise EmptyPageError(
                self._url,
            )
        
        #
        # Нет тега body.
        #
        
        if self._soup.body is None:
            raise EmptyPageError(
                self._url,
            )
        
        #
        # Нет текста.
        #
        
        text = self._soup.get_text(
            " ",
            strip=True,
        )
        
        if not text:
            raise EmptyPageError(
                self._url,
            )
    
    # ------------------------------------------------------------------
    
    # def _check_dynamic_site(
    #         self,
    # ) -> None:
    #     """
    #     Проверить, не является ли страница
    #     JavaScript-приложением.
    #     """
    #     print("dynamic start")
    #     html = self._html.lower()
    #
    #     #
    #     # Известные признаки SPA.
    #     #
    #
    #     markers = (
    #
    #         "__next",
    #
    #         "__nuxt",
    #
    #         "__remix",
    #
    #         "__vite",
    #
    #         "data-reactroot",
    #
    #         "webpack",
    #
    #         "react",
    #
    #         "notion",
    #
    #     )
    #
    #     if any(
    #             marker in html
    #             for marker in markers
    #     ):
    #         print("DynamicSiteError")
    #         raise DynamicSiteError(
    #             self._url,
    #         )
    #
    #     text = self._soup.get_text(
    #         " ",
    #         strip=True,
    #     )
    #
    #     paragraphs = self._soup.find_all(
    #         "p",
    #     )
    #
    #     articles = self._soup.find_all(
    #         "article",
    #     )
    #
    #     mains = self._soup.find_all(
    #         "main",
    #     )
    #
    #     scripts = self._soup.find_all(
    #         "script",
    #     )
    #
    #     #
    #     # Эвристика.
    #     #
    #
    #     if (
    #             len(text) < 300
    #             and len(paragraphs) == 0
    #             and len(articles) == 0
    #             and len(mains) == 0
    #             and len(scripts) > 10
    #     ):
    #         print("dynamic detected")
    #         raise DynamicSiteError(
    #             self._url,
    #         )
    #     print("dynamic finish")