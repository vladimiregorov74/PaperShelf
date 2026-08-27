from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from papershelf.ui.widgets.url_widget import UrlWidget
from papershelf.ui.styles.progress_bar_styles import PROGRESS_BAR_STYLE

class TopPanel(QWidget):
    """
    Верхняя панель приложения.
    """

    save_requested = Signal(str)

    # ------------------------------------------------------------------

    def __init__(self) -> None:
        super().__init__()

        self._create_widgets()
        self.save_button.setFixedWidth(170)
        self._create_layout()
        self._connect_signals()

    # ------------------------------------------------------------------

    def _create_widgets(self) -> None:

        self.url_widget = UrlWidget()

        self.save_button = QPushButton(
            "📥 Сохранить статью"
        )

        self.stage_label = QLabel()
        self.stage_label.setVisible(False)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(10)
        self.progress_bar.setMinimumWidth(300)
        self.progress_bar.setVisible(False)
        self.progress_bar.setStyleSheet(PROGRESS_BAR_STYLE)

    # ------------------------------------------------------------------

    def _create_layout(self) -> None:
        """
        Создание компоновки.
        """

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(4)

        row = QHBoxLayout()
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(8)
        row.addWidget(self.url_widget, 1)
        row.addWidget(self.save_button)

        outer.addLayout(row)
        outer.addWidget(self.stage_label)
        outer.addWidget(self.progress_bar)

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

        self.stage_label.setVisible(busy)
        self.progress_bar.setVisible(busy)

        if not busy:
            self.stage_label.clear()

    # ------------------------------------------------------------------

    def set_stage(
        self,
        stage: str,
    ) -> None:
        """
        Обновить текст текущей стадии.
        """

        self.stage_label.setText(stage)

    # ------------------------------------------------------------------

    def set_url(
            self,
            url: str,
    ) -> None:
        """
        Установить URL.
        """

        self.url_widget.setText(url)