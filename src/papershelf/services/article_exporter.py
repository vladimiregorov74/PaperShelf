from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from papershelf.config.constants import (
    ARTICLE_HTML_FILENAME,
    ARTICLE_JSON_FILENAME,
    SAVE_DIRECTORY,
)
from papershelf.models import Article
from slugify import slugify


class ArticleExporter:
    """
    Сохраняет статью на диск.

    Экспортирует:

    - article.html
    - article.json
    """

    # ------------------------------------------------------------------

    def export(
        self,
        article: Article,
    ) -> Path:
        """
        Экспортировать статью.

        Возвращает путь к созданному каталогу.
        """

        article_dir = self._create_directory(article)

        self._save_html(article, article_dir)

        self._save_json(article, article_dir)

        return article_dir

    # ------------------------------------------------------------------

    def _create_directory(
        self,
        article: Article,
    ) -> Path:
        """
        Создать каталог статьи.
        """

        directory = (
            Path(SAVE_DIRECTORY)
            / slugify(article.title)
        )

        directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        return directory

    # ------------------------------------------------------------------

    def _save_html(
        self,
        article: Article,
        directory: Path,
    ) -> None:
        """
        Сохранить HTML статьи.
        """

        path = directory / ARTICLE_HTML_FILENAME

        html = self._build_html(article)

        path.write_text(
            html,
            encoding="utf-8",
        )

    # ------------------------------------------------------------------

    def _save_json(
        self,
        article: Article,
        directory: Path,
    ) -> None:
        """
        Сохранить метаданные статьи.
        """

        path = directory / ARTICLE_JSON_FILENAME

        data = asdict(article)

        path.write_text(
            json.dumps(
                data,
                indent=4,
                ensure_ascii=False,
                default=str,
            ),
            encoding="utf-8",
        )

    # ------------------------------------------------------------------

    def _build_html(
        self,
        article: Article,
    ) -> str:
        """
        Построить автономную HTML-страницу.
        """

        return f"""<!DOCTYPE html>
<html lang="ru">

<head>

<meta charset="UTF-8">

<title>{article.title}</title>

<style>

body {{

    max-width: 900px;
    margin: auto;
    padding: 40px;

    font-family: Arial, sans-serif;

    line-height: 1.7;

    background: white;

    color: #222;
}}

h1 {{

    margin-bottom: 5px;

}}

.info {{

    color: gray;

    margin-bottom: 40px;

}}

img {{

    max-width: 100%;
}}

pre {{

    overflow-x: auto;

    padding: 15px;

    background: #f5f5f5;

}}

code {{

    font-family: Consolas, monospace;

}}

</style>

</head>

<body>

<h1>{article.title}</h1>

<div class="info">

Автор: {article.author}<br>

Источник:
<a href="{article.url}">
{article.url}
</a>

</div>

{article.html}

</body>

</html>
"""
