from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

from papershelf.parsers import HabrParser
from papershelf.services import (
    ArticleExporter,
    AssetDownloader,
    DownloaderService,
)

Logger = Callable[[str], None]


class ArticleController:
    """
    Главный контроллер сохранения статьи.
    """

    # ------------------------------------------------------------------

    def __init__(self) -> None:

        self._downloader = DownloaderService()

        self._parser = HabrParser()

        self._asset_downloader = AssetDownloader(
            self._downloader,
        )

        self._exporter = ArticleExporter()

    # ------------------------------------------------------------------
    
    def save_article(
            self,
            url: str,
            logger: Logger | None = None,
    ) -> Path:
        """
        Скачать, обработать и сохранить статью.
        """
        
        def log(message: str) -> None:
            if logger:
                logger(message)
        
        html = self._download_html(
            url,
            log,
        )
        
        article = self._parse_article(
            html,
            url,
            log,
        )
        
        directory = self._create_directory(
            article,
            log,
        )
        
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
        
        log("Готово.")
        
        return directory
    
    # ------------------------------------------------------------------
    
    def _download_html(
            self,
            url: str,
            logger: Logger,
    ) -> str:
        """
        Скачать HTML-код страницы.

        Parameters
        ----------
        url:
            Адрес статьи.

        logger:
            Функция вывода сообщений.

        Returns
        -------
        str
            HTML-код страницы.
        """
        
        logger(
            "Загрузка страницы..."
        )
        
        return self._downloader.download(
            url
        )
    
    # ------------------------------------------------------------------
    
    def _parse_article(
            self,
            html: str,
            url: str,
            logger: Logger,
    ):
        """
        Преобразовать HTML страницы в объект статьи.

        Parameters
        ----------
        html:
            HTML-код страницы.

        url:
            Исходный адрес статьи.

        logger:
            Функция вывода сообщений.

        Returns
        -------
        Article
            Распарсенная статья.
        """
        
        logger(
            "Парсинг статьи..."
        )
        
        return self._parser.parse(
            html=html,
            url=url,
        )
    
    # ------------------------------------------------------------------
    
    def _create_directory(
            self,
            article,
            logger: Logger,
    ) -> Path:
        """
        Создать каталог для сохранения статьи.

        Parameters
        ----------
        article:
            Объект статьи.

        logger:
            Функция вывода сообщений.

        Returns
        -------
        Path
            Каталог статьи.
        """
        
        logger(
            "Создание каталога..."
        )
        
        return self._exporter.create_directory(
            article
        )
    
    # ------------------------------------------------------------------
    
    def _download_assets(
            self,
            article,
            directory: Path,
            logger: Logger,
    ) -> None:
        """
        Скачать все изображения статьи.

        Parameters
        ----------
        article:
            Объект статьи.

        directory:
            Каталог сохранения статьи.

        logger:
            Функция вывода сообщений.
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
            article,
            directory: Path,
            logger: Logger,
    ) -> None:
        """
        Сохранить статью на диск.

        Parameters
        ----------
        article:
            Объект статьи.

        directory:
            Каталог сохранения.

        logger:
            Функция вывода сообщений.
        """
        
        logger(
            "Сохранение статьи..."
        )
        
        self._exporter.save(
            article=article,
            directory=directory,
        )