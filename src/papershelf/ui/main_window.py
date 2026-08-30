from __future__ import annotations

from pathlib import Path
from urllib.parse import urlparse

from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices, QCloseEvent
from PySide6.QtWidgets import (
    QDialog,
    QInputDialog,
    QMessageBox,
)

from papershelf.core.exceptions import (
    SiteAnalysisError, DynamicSiteError,
)
from papershelf.config.constants import STATUS_MESSAGE_TIMEOUT, STATUS_MESSAGE_LONG_TIMEOUT


from papershelf.controllers.library_controller import LibraryController
from papershelf.controllers.save_controller import SaveController
from papershelf.core.app_settings import AppSettings
from papershelf.core.paths import SAVED_DIR
from papershelf.models import LibraryItem
from papershelf.services.article_service import ArticleService
from papershelf.services.library_scanner import LibraryScanner
from papershelf.ui.base_window import BaseWindow
from papershelf.ui.builders.main_window_builder import MainWindowBuilder
from papershelf.ui.dialogs.about_dialog import AboutDialog
from papershelf.ui.dialogs.confirm_dialog import ConfirmDialog
from papershelf.ui.dialogs.new_site_dialog import NewSiteDialog
from papershelf.ui.dialogs.settings_dialog import SettingsDialog
from papershelf.controllers import SiteSupportController
from papershelf.ui.dialogs.supported_sites_dialog import SupportedSitesDialog
from tools.site_inspector.naming_utils import guess_source_name


class MainWindow(BaseWindow):
    """
    Главное окно приложения.
    """

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def __init__(self) -> None:
        super().__init__()
        
        self._save_controller = SaveController(
            window=self,
        )
        
        self._library_scanner = LibraryScanner(
            SAVED_DIR,
        )
        
        self._library_controller = LibraryController(
            self._library_scanner,
        )
        
        self._settings = AppSettings()
        
        
        
        # ------------------------------------------------------------------
        # UI
        # ------------------------------------------------------------------
        
        MainWindowBuilder.build(self)
        
        self._save_controller.start()
        
        self._apply_settings()

        articles = self._reload_library()

        if articles:
            first_article = articles[0]

            self._open_article(
                first_article.directory,
            )

            self.library_widget.select_article(
                first_article.directory,
            )
        
        self._site_support_controller = SiteSupportController(
            parent=self,
        )
        
        self._save_controller.unsupported_site.connect(
            self._on_unsupported_site,
        )
        
        self._site_support_controller.completed.connect(
            self._save_controller.retry,
        )
        
        self._site_support_controller.exception.connect(
            self._on_site_support_exception,
        )
        
        self._site_support_controller.error.connect(
            self._on_site_support_error,
        )
        
        self._library_visible = True
        self._update_library_action()

    # ------------------------------------------------------------------
    # Dialogs
    # ------------------------------------------------------------------
    
    def show_about_dialog(self) -> None:
        """
        Показать окно "О программе".
        """
        
        dialog = AboutDialog(
            self,
        )
        
        dialog.exec()

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
    
    def _toggle_library(self) -> None:
        """
        Показать или скрыть панель библиотеки.
        """
        
        left_panel = self.splitter.widget(0)
        
        if left_panel is None:
            return
        
        self._library_visible = not self._library_visible
        
        left_panel.setVisible(self._library_visible)
        
        self._update_library_action()

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
            STATUS_MESSAGE_TIMEOUT,
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
            STATUS_MESSAGE_TIMEOUT,
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
            STATUS_MESSAGE_TIMEOUT,
        )



    # ------------------------------------------------------------------

    def _on_rename_requested(
            self,
            article: LibraryItem,
    ) -> None:
        """
        Изменить название статьи.
        """

        title, accepted = QInputDialog.getText(
            self,
            "Переименовать статью",
            "Название:",
            text=article.title,
        )

        if not accepted:
            return

        title = title.strip()

        if not title:
            QMessageBox.warning(
                self,
                "Некорректное название",
                "Название статьи не может быть пустым.",
            )

            return

        if title == article.title:
            return

        try:
            self._library_controller.rename(
                item=article,
                title=title,
            )

        except Exception as exception:
            self.log_widget.error(
                f"Не удалось переименовать статью: {exception}"
            )

            QMessageBox.critical(
                self,
                "Ошибка",
                str(exception),
            )

            return

        self.log_widget.success(
            f"Статья переименована:\n{title}",
        )

        self._reload_library()

        self.status_bar.showMessage(
            "Название статьи изменено.",
            STATUS_MESSAGE_LONG_TIMEOUT,
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
            STATUS_MESSAGE_LONG_TIMEOUT,
        )
    
    # ------------------------------------------------------------------
    # Dialogs
    # ------------------------------------------------------------------
    
    def _show_settings_dialog(self) -> None:
        """
        Показать окно настроек.
        """
        
        dialog = SettingsDialog(
            file_logging=self._settings.file_logging_enabled(),
            log_panel_visible=self._settings.log_panel_visible(),
            parent=self,
        )
        
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return
        
        file_logging = dialog.file_logging_enabled()
        log_panel_visible = dialog.log_panel_visible()
        
        self._settings.set_file_logging(
            file_logging,
        )
        
        self._settings.set_log_panel_visible(
            log_panel_visible,
        )
        
        self._apply_settings()
        
        self.status_bar.showMessage(
            "Настройки сохранены.",
            STATUS_MESSAGE_TIMEOUT,
        )

    # ------------------------------------------------------------------
    
    def _apply_settings(self) -> None:
        """
        Применить настройки приложения.
        """
        
        self.log_widget.set_file_logging(
            self._settings.file_logging_enabled(),
        )
        
        left_splitter = self.splitter.widget(0)
        
        if left_splitter is not None:
            self.log_widget.setVisible(
                self._settings.log_panel_visible(),
            )

    # ------------------------------------------------------------------
    
    def _on_unsupported_site(
            self,
            url: str,
            page,
    ) -> None:
        """
        Сайт пока не поддерживается.
        """
        
        domain = urlparse(url).netloc
        
        data = NewSiteDialog.ask(
            parent=self,
            source=guess_source_name(domain),
            title_suffix="",
        )
        
        if data is None:
            self.log_widget.info(
                "Добавление поддержки сайта отменено.",
            )
            return
        
        self.top_panel.set_busy(True)
        
        self._site_support_controller.register(
            url=url,
            logger=self.log_widget.info,
            source=data.source,
            title_suffix=data.title_suffix,
            on_stage=self.top_panel.set_stage,
        )
    
    # ------------------------------------------------------------------
    
    def _on_site_support_error(
            self,
            traceback_text: str,
    ) -> None:
        """
        Обработка неожиданных ошибок.
        """
        
        self.log_widget.error(
            traceback_text,
        )
        
        QMessageBox.critical(
            self,
            "Ошибка",
            traceback_text,
        )
        self.top_panel.set_busy(False)
    
    # ------------------------------------------------------------------
    
    def _on_site_support_exception(
            self,
            exception: Exception,
    ) -> None:
        """
        Обработка специальных ошибок
        регистрации сайта.
        """
        
        if isinstance(
                exception,
                DynamicSiteError,
        ):
            message = (
                "Сайт использует динамическую загрузку содержимого "
                "(JavaScript).\n\n"
                "Автоматический анализ пока не поддерживает такие сайты."
            )
            
            self.log_widget.warning(message)
            
            QMessageBox.warning(
                self,
                "Динамический сайт",
                message,
            )
            self.top_panel.set_busy(False)
            return
        
        if isinstance(
                exception,
                SiteAnalysisError,
        ):
            self.log_widget.warning(
                exception.reason,
            )
            
            QMessageBox.warning(
                self,
                "Не удалось зарегистрировать сайт",
                exception.reason,
            )
            self.top_panel.set_busy(False)
            return
    
    def _show_supported_sites(self) -> None:
        """
        Открыть окно управления
        поддерживаемыми сайтами.
        """
        
        dialog = SupportedSitesDialog(
            self,
        )
        
        dialog.exec()
    
    def closeEvent(
            self,
            event: QCloseEvent,
    ) -> None:
        """
        Корректно завершить приложение.
        """
    
        self._save_controller.close()
    
        event.accept()
    
    # ------------------------------------------------------------------
    
    def _update_library_action(self) -> None:
        
        if self._library_visible:
            text = "Скрыть библиотеку"
        else:
            text = "Показать библиотеку"
        
        self.actions.library.setToolTip(text)
        self.actions.library.setStatusTip(text)