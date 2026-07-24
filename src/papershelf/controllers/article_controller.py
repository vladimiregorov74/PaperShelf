from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

from papershelf.parsers import HabrParser
from papershelf.services import (
    ArticleExporter,
    DownloaderService,
)

Logger = Callable[[str], None]


class ArticleController:
    """
    Главный контроллер сохранения статьи.
    """

    def __init__(self) -> None:
        self._downloader = DownloaderService()
        self._parser = HabrParser()
        self._exporter = ArticleExporter()

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

        log("Загрузка страницы...")

        html = self._downloader.download(url)

        log("Парсинг статьи...")

        article = self._parser.parse(
            html=html,
            url=url,
        )

        log("Сохранение статьи...")

        directory = self._exporter.export(article)

        log("Готово.")

        return directory