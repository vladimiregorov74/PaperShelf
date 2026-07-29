from __future__ import annotations

import shutil
from pathlib import Path


class LibraryManager:
    """
    Управление библиотекой статей.
    """

    # ------------------------------------------------------------------

    @staticmethod
    def delete_article(
        directory: Path,
    ) -> None:
        """
        Удалить каталог статьи.
        """

        if not directory.exists():
            return

        shutil.rmtree(directory)