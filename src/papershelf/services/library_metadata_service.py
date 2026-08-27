from __future__ import annotations

import json
from pathlib import Path


class LibraryMetadataService:
    """
    Сервис изменения метаданных сохранённых статей.
    """

    # ------------------------------------------------------------------

    def rename(
        self,
        directory: Path,
        title: str,
    ) -> None:
        """
        Изменить название статьи.

        Parameters
        ----------
        directory:
            Каталог сохранённой статьи.

        title:
            Новое название статьи.
        """

        title = title.strip()

        if not title:
            raise ValueError(
                "Название статьи не может быть пустым."
            )

        article_json = directory / "article.json"

        if not article_json.exists():
            raise FileNotFoundError(
                f"Файл статьи не найден: {article_json}"
            )

        data = json.loads(
            article_json.read_text(
                encoding="utf-8",
            )
        )

        data["title"] = title

        article_json.write_text(
            json.dumps(
                data,
                ensure_ascii=False,
                indent=4,
            ),
            encoding="utf-8",
        )