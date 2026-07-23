from __future__ import annotations

from pathlib import Path

from papershelf.parsers import HabrParser
from papershelf.services import (
    ArticleExporter,
    DownloaderService,
)


class ArticleController:
    """
    Главный контроллер сохранения статьи.
    """

    # ------------------------------------------------------------------

    def __init__(self) -> None:

        self._downloader = DownloaderService()
        self._parser = HabrParser()
        self._exporter = ArticleExporter()

    # ------------------------------------------------------------------

    def save_article(
        self,
        url: str,
    ) -> Path:
        """
        Скачать, обработать и сохранить статью.
        """

        html = self._downloader.download(url)

        article = self._parser.parse(
            html=html,
            url=url,
        )

        return self._exporter.export(article)