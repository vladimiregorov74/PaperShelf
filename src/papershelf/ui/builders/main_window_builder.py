from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QSplitter,
    QStatusBar,
    QVBoxLayout,
    QWidget,
)

from papershelf.config.constants import (
    LOG_PANEL_WIDTH,
    STATUS_READY,
)
from papershelf.ui.actions import create_actions

from papershelf.ui.menu_bar import MainMenuBar
from papershelf.ui.panels.top_panel import TopPanel
from papershelf.ui.toolbar import MainToolBar
from papershelf.ui.widgets.library_panel import LibraryPanel
from papershelf.ui.widgets.log_widget import LogWidget
from papershelf.ui.widgets.preview_widget import PreviewWidget


class MainWindowBuilder:

    @staticmethod
    def build(window) -> None:
        """
        Полностью собрать MainWindow.
        """

        MainWindowBuilder._create_actions(window)
        MainWindowBuilder._create_widgets(window)
        MainWindowBuilder._create_layout(window)
        MainWindowBuilder._connect_signals(window)

    # ------------------------------------------------------------

    @staticmethod
    def _create_actions(window) -> None:
        window.actions = create_actions(window)

    # ------------------------------------------------------------

    @staticmethod
    def _create_widgets(window) -> None:

        window.central_widget = QWidget()

        window.top_panel = TopPanel()

        window.log_widget = LogWidget()

        window.library_widget = LibraryPanel()

        window.preview_widget = PreviewWidget()

        window.splitter = QSplitter(Qt.Orientation.Horizontal)

        window.main_toolbar = MainToolBar(window.actions)
        window.addToolBar(window.main_toolbar)

        window.main_menu = MainMenuBar(window.actions)
        window.setMenuBar(window.main_menu)

        window.status_bar = QStatusBar()
        window.status_bar.showMessage(STATUS_READY)

        window.setStatusBar(window.status_bar)

    # ------------------------------------------------------------

    @staticmethod
    def _create_layout(window) -> None:

        layout = QVBoxLayout(window.central_widget)

        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        layout.addWidget(window.top_panel)

        left_splitter = QSplitter(Qt.Orientation.Vertical)

        left_splitter.addWidget(window.library_widget)
        left_splitter.addWidget(window.log_widget)

        left_splitter.setStretchFactor(0, 3)
        left_splitter.setStretchFactor(1, 2)

        window.splitter.addWidget(left_splitter)
        window.splitter.addWidget(window.preview_widget)

        window.splitter.setStretchFactor(0, 1)
        window.splitter.setStretchFactor(1, 3)

        window.splitter.setSizes(
            [
                LOG_PANEL_WIDTH,
                1000,
            ]
        )

        layout.addWidget(window.splitter, 1)

        window.setCentralWidget(window.central_widget)

    # ------------------------------------------------------------

    @staticmethod
    def _connect_signals(window) -> None:

        window.top_panel.save_requested.connect(
            window._on_save_requested
        )

        window.actions.download.triggered.connect(
            window._download_clicked
        )

        window.library_widget.article_selected.connect(
            window._on_article_selected
        )

        window.library_widget.open_folder_requested.connect(
            window._on_open_folder_requested
        )

        window.library_widget.open_original_requested.connect(
            window._on_open_original_requested
        )

        window.actions.library.triggered.connect(
            window._toggle_library
        )

        window.actions.open_folder.triggered.connect(
            window._open_current_directory
        )

        window.actions.refresh_library.triggered.connect(
            window._reload_library
        )

        window.actions.sort_by_date.triggered.connect(
            window._sort_by_date
        )

        window.actions.sort_by_title.triggered.connect(
            window._sort_by_title
        )
        
        window.actions.settings.triggered.connect(
            window._show_settings_dialog,
        )

        window.library_widget.delete_requested.connect(
            window._on_delete_requested
        )