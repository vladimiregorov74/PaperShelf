from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QTextBrowser


class PreviewWidget(QTextBrowser):
    """
    Виджет предварительного просмотра статьи.
    """

    # ------------------------------------------------------------------

    def __init__(self) -> None:
        super().__init__()

        self.setOpenExternalLinks(True)

        self.setOpenLinks(True)

        self.setReadOnly(True)

        self.setPlaceholderText(
            "Предварительный просмотр статьи"
        )

        self._show_welcome()

    # ------------------------------------------------------------------

    def _show_welcome(self) -> None:
        """
        Показать приветственное сообщение.
        """

        self.setHtml(
            """
            <h2>PaperShelf</h2>

            <p>
                Вставьте ссылку на статью и нажмите
                <b>«Сохранить статью»</b>.
            </p>

            <p>
                После сохранения статья автоматически
                откроется здесь.
            </p>
            """
        )

    # ------------------------------------------------------------------

    def load_article(
        self,
        directory: Path,
    ) -> None:
        """
        Загрузить сохранённую статью.
        """

        html_file = directory / "article.html"

        if not html_file.exists():

            self.setHtml(
                f"""
                <h3>Ошибка</h3>

                <p>

                Не найден файл

                <b>{html_file.name}</b>

                </p>
                """
            )

            return

        self.setSource(
            html_file.resolve().as_uri()
        )

    # ------------------------------------------------------------------

    def clear_preview(self) -> None:
        """
        Очистить область просмотра.
        """

        self._show_welcome()