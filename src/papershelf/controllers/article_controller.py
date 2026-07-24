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

        #
        # Загрузка HTML
        #
        log("Загрузка страницы...")

        html = self._downloader.download(url)

        #
        # Парсинг
        #
        log("Парсинг статьи...")

        article = self._parser.parse(
            html=html,
            url=url,
        )

        #
        # Создание каталога
        #
        log("Создание каталога...")

        directory = self._exporter.create_directory(
            article,
        )

        #
        # Загрузка изображений
        #
        log("Загрузка изображений...")

        self._asset_downloader.process(
            article=article,
            directory=directory,
            logger=log,
        )

        #
        # Сохранение
        #
        log("Сохранение статьи...")

        self._exporter.save(
            article=article,
            directory=directory,
        )

        log("Готово.")

        return directory