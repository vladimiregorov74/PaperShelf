from __future__ import annotations

from PySide6.QtWidgets import QMainWindow

from papershelf.config.constants import (
    APP_NAME,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    MIN_WIDTH,
    MIN_HEIGHT,
)


class BaseWindow(QMainWindow):
    """Базовый класс всех окон."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self._configure()

    def _configure(self) -> None:
        self.setWindowTitle(APP_NAME)

        self.resize(
            WINDOW_WIDTH,
            WINDOW_HEIGHT,
        )

        self.setMinimumSize(
            MIN_WIDTH,
            MIN_HEIGHT,
        )