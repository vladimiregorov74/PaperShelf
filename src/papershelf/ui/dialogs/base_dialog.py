from __future__ import annotations

from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
)


class BaseDialog(QDialog):
    """
    Базовый диалог приложения PaperShelf.

    Является основой для всех диалоговых окон
    приложения.

    Назначение
    ----------
    Обеспечивает единый внешний вид всех диалогов.

    Особенности
    -----------
    • общий заголовок;

    • одинаковые размеры;

    • единые отступы;

    • готовая вертикальная компоновка.
    """

    # ------------------------------------------------------------------

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.main_layout = QVBoxLayout(self)

        self._configure()

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