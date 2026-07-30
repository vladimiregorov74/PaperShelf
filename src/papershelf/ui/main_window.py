
from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import (
    Qt,
    QThread,
)
from PySide6.QtWidgets import (
    QMessageBox,
    QSplitter,
    QStatusBar,
    QVBoxLayout,
    QWidget,
)
from PySide6.QtGui import QDesktopServices
from PySide6.QtCore import QUrl
from papershelf.config.constants import (
    LOG_PANEL_WIDTH,
    STATUS_READY,
)
from papershelf.controllers import ArticleController
from papershelf.services.article_service import ArticleService
from papershelf.ui.base_window import BaseWindow
from papershelf.ui.menu_bar import MainMenuBar
from papershelf.ui.panels.top_panel import TopPanel
from papershelf.ui.toolbar import MainToolBar
from papershelf.ui.widgets.log_widget import LogWidget
from papershelf.ui.widgets.preview_widget import PreviewWidget
from papershelf.workers import SaveArticleWorker
from papershelf.services.library_scanner import LibraryScanner
from papershelf.ui.widgets.library_panel import LibraryPanel
from papershelf.core.paths import SAVED_DIR
from papershelf.ui.dialogs.confirm_dialog import ConfirmDialog





class MainWindow(BaseWindow):
    """
    Главное окно приложения.
    """

    def __init__(self) -> None:
        super().__init__()

        self._controller = ArticleController()
        self._library_scanner = LibraryScanner(
            SAVED_DIR,
        )
        self._sort_mode = "date"
        self._worker: SaveArticleWorker | None = None
        
        self._thread: QThread | None = None

        self._create_actions()
        self._create_widgets()
        self._create_layout()
        self._connect_signals()
        articles = self._reload_library()
        
        if articles:
            self._open_article(
                articles[0].directory
            )
            
            self.library_widget.select_article(
                articles[0].directory
            )

    # ------------------------------------------------------------------

    def _create_actions(self) -> None:
        from papershelf.ui.actions import create_actions

        self.actions = create_actions(self)

    # ------------------------------------------------------------------

    def _create_widgets(self) -> None:

        self.central_widget = QWidget()

        self.top_panel = TopPanel()

        self.log_widget = LogWidget()
        
        self.library_widget = LibraryPanel()

        self.preview_widget = PreviewWidget()

        self.splitter = QSplitter(Qt.Orientation.Horizontal)

        self.main_toolbar = MainToolBar(self.actions)
        self.addToolBar(self.main_toolbar)

        self.main_menu = MainMenuBar(self.actions)
        self.setMenuBar(self.main_menu)

        self.status_bar = QStatusBar()
        self.status_bar.showMessage(STATUS_READY)

        self.setStatusBar(self.status_bar)

    # ------------------------------------------------------------------

    def _create_layout(self) -> None:

        layout = QVBoxLayout(self.central_widget)

        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        layout.addWidget(self.top_panel, 0,)
        
        left_splitter = QSplitter(Qt.Orientation.Vertical)
        
        left_splitter.addWidget(
            self.library_widget
        )
        
        left_splitter.addWidget(
            self.log_widget
        )
        
        left_splitter.setStretchFactor(
            0,
            3,
        )
        
        left_splitter.setStretchFactor(
            1,
            2,
        )
        
        self.splitter.addWidget(
            left_splitter
        )
        
        self.splitter.addWidget(
            self.preview_widget
        )
        
        self.splitter.setStretchFactor(
            0,
            1,
        )
        
        self.splitter.setStretchFactor(
            1,
            3,
        )
        
        self.splitter.setSizes(
            [
                LOG_PANEL_WIDTH,
                1000,
            ]
        )

        layout.addWidget(self.splitter, 1,)

        self.setCentralWidget(self.central_widget)
    
    # ------------------------------------------------------------------

    def _connect_signals(self) -> None:
        """
        Подключение сигналов.
        """

        self.top_panel.save_requested.connect(
            self._on_save_requested
        )
        
        self.actions.download.triggered.connect(
            self._download_clicked
        )
        
        self.library_widget.article_selected.connect(
            self._on_article_selected
        )
        
        self.library_widget.open_folder_requested.connect(
            self._on_open_folder_requested
        )
        
        self.library_widget.open_original_requested.connect(
            self._on_open_original_requested
        )
        #
        # Действия меню и панели инструментов
        #
        self.actions.library.triggered.connect(
            self._toggle_library
        )
        self.actions.open_folder.triggered.connect(
            self._open_current_directory
        )
        
        self.actions.refresh_library.triggered.connect(
            self._reload_library
        )
        
        self.actions.sort_by_date.triggered.connect(
            self._sort_by_date
        )
        
        self.actions.sort_by_title.triggered.connect(
            self._sort_by_title
        )
        
        self.library_widget.delete_requested.connect(
            self._on_delete_requested
        )
    # ------------------------------------------------------------------
    
    def _download_clicked(self) -> None:
        """
        Скачать статью через кнопку панели инструментов.
        """
        
        self._on_save_requested(
            self.top_panel.url_widget.text()
        )

    # ------------------------------------------------------------------

    def show_about_dialog(self) -> None:
        """
        Окно "О программе".
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
    
    def _on_save_requested(
            self,
            url: str,
    ) -> None:
        """
        Пользователь нажал кнопку сохранения.
        """
        
        url = url.strip()
        
        if not url:
            QMessageBox.warning(
                self,
                "Пустой URL",
                "Введите адрес статьи.",
            )
            return
        
        self.top_panel.set_busy(True)
        
        self.log_widget.info(
            f"Получен URL: {url}"
        )
        
        self.status_bar.showMessage(
            "Сохранение статьи..."
        )
        
        self._thread = QThread(self)
        
        self._worker = SaveArticleWorker(
            controller=self._controller,
            url=url,
        )
        
        self._worker.moveToThread(self._thread)
        
        #
        # Запуск
        #
        self._thread.started.connect(
            self._worker.run
        )
        
        #
        # Логирование
        #
        self._worker.log.connect(
            self.log_widget.info
        )
        
        #
        # Успешное завершение
        #
        self._worker.success.connect(
            self._on_worker_success
        )
        
        #
        # Ошибка
        #
        self._worker.error.connect(
            self._on_worker_error
        )
        
        #
        # Завершение
        #
        self._worker.finished.connect(
            self._on_worker_finished
        )
        
        #
        # Корректное закрытие потока
        #
        self._worker.finished.connect(
            self._thread.quit
        )
        
        self._worker.finished.connect(
            self._worker.deleteLater
        )
        
        self._thread.finished.connect(
            self._thread.deleteLater
        )
        
        self._thread.start()
        
    # ------------------------------------------------------------------
    
    def _on_worker_success(
            self,
            directory,
    ) -> None:
        """
        Статья успешно сохранена.
        """
        
        self.log_widget.success(
            f"Статья успешно сохранена:\n{directory}"
        )
        
        self._reload_library()
        
        self.library_widget.select_article(
            directory
        )
        
        self.status_bar.showMessage(
            "Статья сохранена.",
            5000,
        )

    # ------------------------------------------------------------------

    def _on_worker_error(
        self,
        traceback_text: str,
    ) -> None:
        """
        Ошибка при сохранении.
        """

        self.log_widget.error(
            traceback_text
        )

        QMessageBox.critical(
            self,
            "Ошибка",
            traceback_text,
        )

        self.status_bar.showMessage(
            "Ошибка сохранения.",
            5000,
        )

    # ------------------------------------------------------------------
    
    def _on_worker_finished(self) -> None:
        """
        Завершение работы Worker.
        """
        
        self.top_panel.set_busy(False)
        
        self.status_bar.showMessage(
            "Готово.",
            3000,
        )
        
        self._worker = None
        self._thread = None
    
    # ------------------------------------------------------------------
    
    def _on_article_selected(
            self,
            article,
    ) -> None:
        """
        Пользователь выбрал статью в библиотеке.
        """
        
        self._open_article(
            article.directory
        )
        
        self.status_bar.showMessage(
            article.title,
            3000,
        )
    
    # ------------------------------------------------------------------
    
    def _open_article(
            self,
            directory: Path,
    ) -> None:
        self.preview_widget.load_article(directory)
    
    # ------------------------------------------------------------------
    
    def _reload_library(self) -> list:
        """
        Перезагрузить библиотеку.
        """
        current = self.library_widget.current_article()
        articles = self._library_scanner.scan(
            sort_by=self._sort_mode,
        )
        
        self.library_widget.set_articles(
            articles
        )
        if current is not None:
            self.library_widget.select_article(
                current.directory
            )
        return articles
    
    # ------------------------------------------------------------------
    
    def _toggle_library(self) -> None:
        """
        Показать или скрыть библиотеку.
        """
        
        left_panel = self.splitter.widget(0)
        
        if left_panel is None:
            return
        
        left_panel.setVisible(
            not left_panel.isVisible()
        )
    
    # ------------------------------------------------------------------
    
    def _open_current_directory(self) -> None:
        """
        Открыть каталог текущей статьи.
        """
        
        item = self.library_widget.current_article()
        
        if item is None:
            QMessageBox.information(
                self,
                "Нет выбранной статьи",
                "Выберите статью в библиотеке.",
            )
            
            return
        
        ArticleService.open_directory(
            item.directory
        )
    
    # ------------------------------------------------------------------
    
    def _sort_by_date(self) -> None:
        """
        Сортировка библиотеки по дате.
        """
        
        self._sort_mode = "date"
        
        self._reload_library()
        
        self.status_bar.showMessage(
            "Сортировка: по дате",
            3000,
        )
    
    # ------------------------------------------------------------------
    
    def _sort_by_title(self) -> None:
        """
        Сортировка библиотеки по названию.
        """
        
        self._sort_mode = "title"
        
        self._reload_library()
        
        self.status_bar.showMessage(
            "Сортировка: по названию",
            3000,
        )
    
    # ------------------------------------------------------------------
    
    def _on_open_folder_requested(
            self,
            article,
    ) -> None:
        """
        Открыть каталог статьи.
        """
        
        QDesktopServices.openUrl(
            QUrl.fromLocalFile(
                str(article.directory)
            )
        )
    
    # ------------------------------------------------------------------
    
    def _on_open_original_requested(
            self,
            article,
    ) -> None:
        """
        Открыть оригинальную статью в браузере.
        """
        
        if not article.url:
            return
        
        QDesktopServices.openUrl(
            QUrl(article.url)
        )
    
    # ------------------------------------------------------------------
    
    def _on_delete_requested(
            self,
            article,
    ) -> None:
        """
        Запрос на удаление статьи.
        """
        
        if not ConfirmDialog.ask(
                parent=self,
                title="Удаление статьи",
                text=article.title,
        ):
            return
        
        ArticleService.delete_article(
            article.directory
        )
        
        self.log_widget.success(
            f"Статья удалена:\n{article.title}"
        )
        
        self._reload_library()
        
        # очистка поля просмотра статьи
        self.preview_widget.clear_preview()
        
        self.status_bar.showMessage(
            "Статья удалена.",
            5000,
        )