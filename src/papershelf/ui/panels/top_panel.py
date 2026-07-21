from __future__ import annotations

from PySide6.QtWidgets import (
    QLabel,
    QPushButton,
    QProgressBar,
    QVBoxLayout,
    QWidget,
)

from papershelf.ui.widgets.url_widget import UrlWidget


class TopPanel(QWidget):
    """Верхняя панель приложения."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self._create_widgets()
        self._create_layout()

    # ------------------------------------------------------------------

    def _create_widgets(self) -> None:

        self.url_label = QLabel("URL статьи")

        self.url_edit = UrlWidget()

        self.download_button = QPushButton("📥 Скачать")

        self.progress_bar = QProgressBar()
        self.progress_bar.hide()

    # ------------------------------------------------------------------

    def _create_layout(self) -> None:

        layout = QVBoxLayout(self)

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        layout.addWidget(self.url_label)
        layout.addWidget(self.url_edit)
        layout.addWidget(self.download_button)
        layout.addWidget(self.progress_bar)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def url(self) -> str:
        """Вернуть введённый URL."""

        return self.url_edit.url()

    def set_progress(self, value: int) -> None:
        """Установить значение прогресса."""

        self.progress_bar.setValue(value)

    def show_progress(self) -> None:
        self.progress_bar.show()

    def hide_progress(self) -> None:
        self.progress_bar.hide()
