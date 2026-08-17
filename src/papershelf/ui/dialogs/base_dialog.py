from __future__ import annotations

from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
)


class BaseDialog(QDialog):
    """
    Базовый диалог приложения PaperShelf.

    Является основой для всех диалоговых окон приложения.
    Обеспечивает единый внешний вид и общие элементы интерфейса.
    """

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def __init__(
        self,
        parent=None,
    ) -> None:
        super().__init__(parent)

        self.main_layout = QVBoxLayout(self)

        self._configure()

    # ------------------------------------------------------------------
    # Configuration
    # ------------------------------------------------------------------

    def _configure(self) -> None:
        """
        Настроить внешний вид окна.
        """

        self.setWindowTitle("PaperShelf")

        self.setMinimumWidth(430)

        self.main_layout.setContentsMargins(
            20,
            20,
            20,
            20,
        )

        self.main_layout.setSpacing(16)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def create_section_title(
        self,
        text: str,
    ) -> QLabel:
        """
        Создать заголовок раздела.

        Parameters
        ----------
        text:
            Текст заголовка.

        Returns
        -------
        QLabel
            Настроенный виджет заголовка.
        """

        label = QLabel(text)

        font = label.font()
        font.setBold(True)
        font.setPointSize(
            font.pointSize() + 1,
        )

        label.setFont(font)

        return label

    # ------------------------------------------------------------------

    def add_buttons(
        self,
        *buttons: QPushButton,
    ) -> None:
        """
        Добавить панель кнопок.

        Parameters
        ----------
        *buttons:
            Кнопки, отображаемые справа налево.
        """

        layout = QHBoxLayout()

        layout.addStretch()

        for button in buttons:
            layout.addWidget(button)

        self.main_layout.addLayout(layout)