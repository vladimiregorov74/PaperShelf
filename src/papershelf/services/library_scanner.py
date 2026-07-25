from __future__ import annotations

import json
from pathlib import Path

from papershelf.models import LibraryItem


class LibraryScanner:
    """
    Сканирует библиотеку сохранённых статей.
    """

    # ------------------------------------------------------------------

    def __init__(
        self,
        library_directory: Path,
    ) -> None:

        self._library_directory = library_directory

    # ------------------------------------------------------------------

    def scan(self) -> list[LibraryItem]:
        """
        Просканировать библиотеку.
        """

        items: list[LibraryItem] = []

        if not self._library_directory.exists():
            return items

        for directory in self._library_directory.iterdir():

            if not directory.is_dir():
                continue

            article_json = directory / "article.json"

            if not article_json.exists():
                continue

            try:

                data = json.loads(
                    article_json.read_text(
                        encoding="utf-8",
                    )
                )

                items.append(
                    LibraryItem(
                        title=data.get(
                            "title",
                            "Без названия",
                        ),
                        author=data.get(
                            "author",
                            "",
                        ),
                        source=data.get(
                            "source",
                            "",
                        ),
                        directory=directory,
                        created_at=data.get(
                            "created_at",
                            "",
                        ),
                    )
                )

            except Exception:

                #
                # Повреждённую статью пропускаем.
                #
                continue

        items.sort(
            key=lambda item: item.created_at,
            reverse=True,
        )

        return items