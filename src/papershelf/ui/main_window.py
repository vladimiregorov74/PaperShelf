from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QMessageBox,
    QSplitter,
    QStatusBar,
    QVBoxLayout,
    QWidget,
)

from papershelf.config.constants import LOG_PANEL_WIDTH, STATUS_READY
from papershelf.ui.base_window import BaseWindow
from papershelf.ui.menu_bar import MainMenuBar
from papershelf.ui.panels.top_panel import TopPanel
from papershelf.ui.toolbar import MainToolBar
from papershelf.ui.widgets.log_widget import LogWidget
from papershelf.ui.widgets.preview_widget import PreviewWidget


class MainWindow(BaseWindow):
    """Главное окно приложения."""

    def __init__(self) -> None:
        super().__init__()

        self._create_actions()
        self._create_widgets()
        self._create_layout()
        self._connect_signals()

    # ------------------------------------------------------------------

    def _create_actions(self) -> None:
        from papershelf.ui.actions import create_actions

        self.actions = create_actions(self)

    # ------------------------------------------------------------------

    def _create_widgets(self) -> None:

        self.central_widget = QWidget()

        self.top_panel = TopPanel()

        self.log_widget = LogWidget()

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

        layout.addWidget(self.top_panel)

        self.splitter.addWidget(self.log_widget)
        self.splitter.addWidget(self.preview_widget)

        self.splitter.setStretchFactor(0, 1)
        self.splitter.setStretchFactor(1, 3)

        self.splitter.setSizes(
            [
                LOG_PANEL_WIDTH,
                1000,
            ]
        )

        layout.addWidget(self.splitter)

        self.setCentralWidget(self.central_widget)

    # ------------------------------------------------------------------

    def _connect_signals(self) -> None:

        self.actions.exit.triggered.connect(self.close)

        self.actions.about.triggered.connect(
            self.show_about_dialog
        )

        self.top_panel.download_button.clicked.connect(
            self._download_clicked
        )

    # ------------------------------------------------------------------

    def _download_clicked(self) -> None:
        """Временный обработчик кнопки."""

        url = self.top_panel.url()

        self.log_widget.info(f"URL: {url}")

    # ------------------------------------------------------------------

    def show_about_dialog(self) -> None:

        QMessageBox.about(
            self,
            "О программе",
            (
                "<h2>PaperShelf</h2>"
                "<p>Версия 0.1.0</p>"
                "<p>Настольное приложение для хранения "
                "технических статей.</p>"
            ),
        )