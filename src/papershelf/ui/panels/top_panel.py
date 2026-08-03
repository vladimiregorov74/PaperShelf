from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QHBoxLayout,
    QPushButton,
    QWidget,
)

from papershelf.ui.widgets.url_widget import UrlWidget


class TopPanel(QWidget):
    """
    Верхняя панель приложения.
    """

    save_requested = Signal(str)

    # ------------------------------------------------------------------

    def __init__(self) -> None:
        super().__init__()

        self._create_widgets()
        self.save_button.setFixedWidth(
            170
        )
        self._create_layout()
        self._connect_signals()

    # ------------------------------------------------------------------

    def _create_widgets(self) -> None:

        self.url_widget = UrlWidget()

        self.save_button = QPushButton(
            "📥 Сохранить статью"
        )

    # ------------------------------------------------------------------

    def _create_layout(self) -> None:
        """
        Создание компоновки.
        """

        layout = QHBoxLayout(self)

        layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        layout.setSpacing(8)

        layout.addWidget(
            self.url_widget,
            1,
        )

        layout.addWidget(
            self.save_button,
        )

    # ------------------------------------------------------------------

    def _connect_signals(self) -> None:

        self.save_button.clicked.connect(
            self._on_save_clicked
        )

    # ------------------------------------------------------------------

    def _on_save_clicked(self) -> None:

        url = self.url_widget.text().strip()

        if not url:
            return

        self.save_requested.emit(url)

    # ------------------------------------------------------------------

    def url(self) -> str:
        """
		Вернуть введённый URL.
		"""

        return self.url_widget.text().strip()
    
    # ------------------------------------------------------------------

    def set_busy(
        self,
        busy: bool,
    ) -> None:
        """
        Заблокировать элементы управления.
        """

        self.url_widget.setEnabled(not busy)

        self.save_button.setEnabled(not busy)

    # ------------------------------------------------------------------

    def set_url(
            self,
            url: str,
    ) -> None:
        """
        Установить URL.
        """

        self.url_widget.setText(url)