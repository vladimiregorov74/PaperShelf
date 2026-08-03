from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import (
    QMessageBox,
)


from papershelf.controllers.article_controller import ArticleController
from papershelf.controllers.library_controller import LibraryController
from papershelf.controllers.save_controller import SaveController
from papershelf.core.paths import SAVED_DIR
from papershelf.models import LibraryItem
from papershelf.services.article_service import ArticleService
from papershelf.services.library_scanner import LibraryScanner
from papershelf.ui.base_window import BaseWindow
from papershelf.ui.builders.main_window_builder import MainWindowBuilder
from papershelf.ui.dialogs.confirm_dialog import ConfirmDialog


class MainWindow(BaseWindow):
    """
    Главное окно приложения.
    """

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def __init__(self) -> None:
        super().__init__()

        self._controller = ArticleController()

        self._save_controller = SaveController(
            window=self,
            controller=self._controller,
        )

        self._library_scanner = LibraryScanner(
            SAVED_DIR,
        )

        self._library_controller = LibraryController(
            self._library_scanner,
        )

        MainWindowBuilder.build(self)

        articles = self._reload_library()

        if articles:
            first_article = articles[0]

            self._open_article(
                first_article.directory,
            )

            self.library_widget.select_article(
                first_article.directory,
            )

    # ------------------------------------------------------------------
    # Dialogs
    # ------------------------------------------------------------------

    def show_about_dialog(self) -> None:
        """
        Показать окно "О программе".
        """

        QMessageBox.about(
            self,
            "О программе",
            (
                "<h2>PaperShelf</h2>"
                "<p>Версия 0.1.0</p>"
                "<p>Настольное приложение "
                "для хранения технических статей.</p>"
            ),
        )

    # ------------------------------------------------------------------
    # Save
    # ------------------------------------------------------------------

    def _on_save_requested(
        self,
        url: str,
    ) -> None:
        """
        Пользователь нажал кнопку сохранения.
        """

        self._save_controller.save(
            url,
        )

    # ------------------------------------------------------------------

    def _download_clicked(self) -> None:
        """
        Сохранить статью через кнопку панели инструментов.
        """

        self._save_controller.save(
            self.top_panel.url(),
        )

    # ------------------------------------------------------------------
    # Library
    # ------------------------------------------------------------------

    def _reload_library(
        self,
    ) -> list[LibraryItem]:
        """
        Перезагрузить библиотеку.

        Returns
        -------
        list[LibraryItem]
            Список статей.
        """

        return self._update_library(
            self._library_controller.reload(),
        )

    # ------------------------------------------------------------------

    def _update_library(
        self,
        articles: list[LibraryItem],
    ) -> list[LibraryItem]:
        """
        Обновить список статей библиотеки.

        Parameters
        ----------
        articles:
            Новый список статей.

        Returns
        -------
        list[LibraryItem]
            Переданный список статей.
        """

        current = self.library_widget.current_article()

        self.library_widget.set_articles(
            articles,
        )

        if current is not None:
            self.library_widget.select_article(
                current.directory,
            )

        return articles

    # ------------------------------------------------------------------

    def _toggle_library(
        self,
    ) -> None:
        """
        Показать или скрыть панель библиотеки.
        """

        left_panel = self.splitter.widget(0)

        if left_panel is None:
            return

        left_panel.setVisible(
            not left_panel.isVisible(),
        )

    # ------------------------------------------------------------------

    def _sort_by_date(
        self,
    ) -> None:
        """
        Сортировка библиотеки по дате.
        """

        self._update_library(
            self._library_controller.sort_by_date(),
        )

        self.status_bar.showMessage(
            "Сортировка по дате.",
            3000,
        )

    # ------------------------------------------------------------------

    def _sort_by_title(
        self,
    ) -> None:
        """
        Сортировка библиотеки по названию.
        """

        self._update_library(
            self._library_controller.sort_by_title(),
        )

        self.status_bar.showMessage(
            "Сортировка по названию.",
            3000,
        )

    # ------------------------------------------------------------------

    def _on_open_folder_requested(
        self,
        article: LibraryItem,
    ) -> None:
        """
        Открыть каталог статьи.
        """

        QDesktopServices.openUrl(
            QUrl.fromLocalFile(
                str(article.directory),
            )
        )

    # ------------------------------------------------------------------

    def _on_open_original_requested(
        self,
        article: LibraryItem,
    ) -> None:
        """
        Открыть оригинальную статью в браузере.
        """

        if not article.url:
            return

        QDesktopServices.openUrl(
            QUrl(
                article.url,
            )
        )
    
    # ------------------------------------------------------------------
    # Article
    # ------------------------------------------------------------------

    def _open_current_directory(
        self,
    ) -> None:
        """
        Открыть каталог текущей статьи.
        """

        article = self.library_widget.current_article()

        if article is None:
            QMessageBox.information(
                self,
                "Нет выбранной статьи",
                "Выберите статью в библиотеке.",
            )

            return

        ArticleService.open_directory(
            article.directory,
        )

    # ------------------------------------------------------------------

    def _open_article(
        self,
        directory: Path,
    ) -> None:
        """
        Открыть статью в области просмотра.

        Parameters
        ----------
        directory:
            Каталог статьи.
        """

        if not ArticleService.article_exists(
            directory,
        ):
            return

        self.preview_widget.load_article(
            directory,
        )

    # ------------------------------------------------------------------

    def _on_article_selected(
        self,
        article: LibraryItem,
    ) -> None:
        """
        Пользователь выбрал статью в библиотеке.

        Parameters
        ----------
        article:
            Выбранная статья.
        """

        self._open_article(
            article.directory,
        )

        self.status_bar.showMessage(
            article.title,
            3000,
        )

    # ------------------------------------------------------------------

    def _on_delete_requested(
        self,
        article: LibraryItem,
    ) -> None:
        """
        Запрос на удаление статьи.

        Parameters
        ----------
        article:
            Статья для удаления.
        """

        if not ConfirmDialog.ask(
            parent=self,
            title="Удаление статьи",
            text=article.title,
        ):
            return

        ArticleService.delete_article(
            article.directory,
        )

        self.log_widget.success(
            f"Статья удалена:\n{article.title}",
        )

        self._reload_library()

        self.preview_widget.clear_preview()

        self.status_bar.showMessage(
            "Статья удалена.",
            5000,
        )

    # ------------------------------------------------------------------