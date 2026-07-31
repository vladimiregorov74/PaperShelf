from __future__ import annotations

from pathlib import Path

from papershelf.services.file_opener import FileOpener
from papershelf.services.library_manager import LibraryManager


class ArticleService:
    """
    Сервис работы со статьями.

    Является фасадом над всеми сервисами,
    которые работают с сохранёнными статьями.

    MainWindow обращается только к ArticleService,
    не зная, какой именно сервис выполняет работу.
    """

    @staticmethod
    def delete_article(
        directory: Path,
    ) -> None:
        """
        Удалить статью.
        """

        LibraryManager.delete_article(
            directory
        )

    @staticmethod
    def open_directory(
        directory: Path,
    ) -> None:
        """
        Открыть каталог статьи.
        """

        FileOpener.open_directory(
            directory
        )
        
    # ------------------------------------------------------------------

    @staticmethod
    def article_exists(
        directory: Path,
    ) -> bool:
        """
        Проверить существование статьи.

        Parameters
        ----------
        directory:
            Каталог статьи.

        Returns
        -------
        bool
            True, если статья существует.
        """

        return directory.exists()