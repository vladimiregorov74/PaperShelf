from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

from papershelf.core.exceptions import UnsupportedSiteError, StaleSelectorsError
from papershelf.loaders.smart_loader import SmartLoader
from papershelf.models import Article
from papershelf.models.loaded_page import LoadedPage
from papershelf.parsers.parser_factory import ParserFactory
from papershelf.services.article_exporter import ArticleExporter
from papershelf.services.asset_downloader import AssetDownloader
from papershelf.services.downloader import DownloaderService

Logger = Callable[[str], None]
StageCallback = Callable[[str], None]

class ArticleController:
    """
    Главный контроллер сохранения статьи.
    """

    # ------------------------------------------------------------------

    def __init__(self) -> None:
        self._loader = SmartLoader()

        self._downloader = DownloaderService()

        self._asset_downloader = AssetDownloader(
            self._downloader,
        )

        self._exporter = ArticleExporter()

    # ------------------------------------------------------------------
    
    def save_article(
            self,
            url: str,
            logger: Logger | None = None,
            on_stage: StageCallback | None = None,
    ) -> Path:
        """
        Скачать, обработать и сохранить статью.
        """

        log = logger or (lambda message: None)
        stage = on_stage or (lambda name: None)

        log(
            "ArticleController.save_article(): START"
        )

        stage("Предзагрузка")

        page = self._download_html(
            url,
            log,
        )

        stage("Анализ")

        article = self._parse_article(
            page,
            log,
        )

        directory = self._create_directory(
            article,
            log,
        )

        stage("Скачивание")

        self._download_assets(
            article,
            directory,
            log,
        )

        self._export_article(
            article,
            directory,
            log,
        )

        log(
            "ArticleController.save_article(): END"
        )

        return directory

    # ------------------------------------------------------------------
    
    def _download_html(
            self,
            url: str,
            logger: Logger,
    ) -> LoadedPage:
        """
        Скачать HTML-код страницы.
        """
        
        logger(
            "ArticleController._download_html(): START"
        )
        
        logger(
            f"loader id={id(self._loader)}"
        )
        
        logger(
            "Вызываем SmartLoader.load()"
        )
        
        page = self._loader.load(
            url,
        )
        
        logger(
            "SmartLoader.load() завершён"
        )
        
        logger(
            f"page id={id(page)}"
        )
        
        logger(
            f"page.url={page.url}"
        )
        
        logger(
            f"HTML length={len(page.html)}"
        )
        
        logger(
            "ArticleController._download_html(): END"
        )
        
        return page

    # ------------------------------------------------------------------
    
    def _parse_article(
            self,
            page: LoadedPage,
            logger: Logger,
    ) -> Article:
        """
        Преобразовать HTML страницы в объект статьи.

        Raises
        ------
        UnsupportedSiteError
            Если для сайта нет зарегистрированного парсера.

        StaleSelectorsError
            Если парсер найден, но статья получена пустой —
            вероятно, структура сайта изменилась и сохранённые
            селекторы устарели.

        Parameters
        ----------
        page:
            Загруженная страница.

        logger:
            Функция для вывода логов.

        Returns
        -------
        Article
        """
        logger("Парсинг статьи...")
        
        try:
            parser = ParserFactory.create(page.url)
        
        except UnsupportedSiteError as exception:
            raise UnsupportedSiteError(
                url=exception.url,
                page=page,
            ) from exception
        
        article = parser.parse(
            html=page.html,
            url=page.url,
        )
        
        if not article.html.strip():
            raise StaleSelectorsError(
                url=page.url,
                identifier=parser.config.identifier,
                source=parser.config.source,
            )
        
        return article

    # ------------------------------------------------------------------

    def _create_directory(
        self,
        article: Article,
        logger: Logger,
    ) -> Path:
        """
        Создать каталог для сохранения статьи.
        """

        logger(
            "Создание каталога..."
        )

        return self._exporter.create_directory(
            article,
        )

    # ------------------------------------------------------------------

    def _download_assets(
        self,
        article: Article,
        directory: Path,
        logger: Logger,
    ) -> None:
        """
        Скачать все изображения статьи.
        """

        logger(
            "Загрузка изображений..."
        )

        self._asset_downloader.process(
            article=article,
            directory=directory,
            logger=logger,
        )

    # ------------------------------------------------------------------

    def _export_article(
        self,
        article: Article,
        directory: Path,
        logger: Logger,
    ) -> None:
        """
        Сохранить статью на диск.
        """

        logger(
            "Сохранение статьи..."
        )

        self._exporter.save(
            article=article,
            directory=directory,
        )

    # ------------------------------------------------------------------

    def close(self) -> None:
        """
        Освободить ресурсы контроллера.
        """

        self._loader.close()