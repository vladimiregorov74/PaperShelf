from __future__ import annotations

from pathlib import Path

from papershelf.models.library_statistics import LibraryStatistics


class LibraryStatisticsService:
    """
    Собирает статистику библиотеки.
    """

    # ------------------------------------------------------------------

    def collect(
        self,
        library_directory: Path,
    ) -> LibraryStatistics:
        """
        Собрать статистику библиотеки.
        """

        article_count = 0
        library_size = 0

        if not library_directory.exists():
            return LibraryStatistics(
                article_count=0,
                library_size=0,
            )

        for directory in library_directory.iterdir():

            if not directory.is_dir():
                continue

            article_json = directory / "article.json"

            if not article_json.exists():
                continue

            article_count += 1

            library_size += self._directory_size(
                directory,
            )

        return LibraryStatistics(
            article_count=article_count,
            library_size=library_size,
        )

    # ------------------------------------------------------------------

    @staticmethod
    def _directory_size(
        directory: Path,
    ) -> int:
        """
        Размер каталога в байтах.
        """

        size = 0

        for path in directory.rglob("*"):

            if path.is_file():
                size += path.stat().st_size

        return size