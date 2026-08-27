from __future__ import annotations

from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
)

from papershelf.config.constants import APP_VERSION
from papershelf.core.paths import SAVED_DIR
from papershelf.core.size_formatter import SizeFormatter
from papershelf.services.library_statistics_service import (
    LibraryStatisticsService,
)


class AboutDialog(QDialog):
    """
    Диалог "О программе".
    """

    # ------------------------------------------------------------------

    def __init__(
        self,
        parent=None,
    ) -> None:
        super().__init__(parent)

        self.setWindowTitle(
            "О программе",
        )

        self.setMinimumWidth(
            480,
        )

        self._statistics_service = (
            LibraryStatisticsService()
        )

        self._create_widgets()
        self._create_layout()
        self._load_statistics()

    # ------------------------------------------------------------------

    def _create_widgets(self) -> None:
        """
        Создать элементы интерфейса.
        """

        self._title = QLabel(
            "<h2>📚 PaperShelf</h2>"
        )

        self._version = QLabel(
            f"Версия {APP_VERSION}"
        )

        self._description = QLabel(
            "Настольное приложение для сохранения "
            "и чтения технических статей."
        )

        self._statistics_title = QLabel(
            "<b>Статистика библиотеки</b>"
        )

        self._article_count = QLabel()

        self._library_size = QLabel()

        self._technology = QLabel(
            "Python 3.12<br>"
            "PySide6<br>"
            "Playwright<br>"
            "BeautifulSoup4<br>"
            "lxml"
        )

        self._library_path = QLabel(
            f"<b>Библиотека:</b><br>{SAVED_DIR}"
        )

        self._close_button = QPushButton(
            "Закрыть",
        )

        self._close_button.clicked.connect(
            self.accept,
        )

    # ------------------------------------------------------------------

    def _create_layout(self) -> None:
        """
        Создать компоновку диалога.
        """

        buttons_layout = QHBoxLayout()

        buttons_layout.addStretch()

        buttons_layout.addWidget(
            self._close_button,
        )

        layout = QVBoxLayout(self)

        layout.addWidget(
            self._title,
        )

        layout.addWidget(
            self._version,
        )

        layout.addSpacing(
            10,
        )

        layout.addWidget(
            self._description,
        )

        layout.addSpacing(
            20,
        )

        layout.addWidget(
            self._statistics_title,
        )

        layout.addWidget(
            self._article_count,
        )

        layout.addWidget(
            self._library_size,
        )

        layout.addSpacing(
            20,
        )

        layout.addWidget(
            QLabel("<b>Используемые технологии</b>"),
        )

        layout.addWidget(
            self._technology,
        )

        layout.addSpacing(
            20,
        )

        layout.addWidget(
            self._library_path,
        )

        layout.addStretch()

        layout.addLayout(
            buttons_layout,
        )

    # ------------------------------------------------------------------

    def _load_statistics(self) -> None:
        """
        Загрузить статистику библиотеки.
        """

        statistics = self._statistics_service.collect(
            SAVED_DIR,
        )

        library_size = SizeFormatter.format(
            statistics.library_size,
        )

        self._article_count.setText(
            f"Статей в библиотеке: "
            f"{statistics.article_count}"
        )

        self._library_size.setText(
            f"Размер библиотеки: "
            f"{library_size}"
        )