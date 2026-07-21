from __future__ import annotations

from PySide6.QtWidgets import QPlainTextEdit


class LogWidget(QPlainTextEdit):
    """Журнал приложения."""

    def __init__(self) -> None:
        super().__init__()

        self._configure()

    def _configure(self) -> None:
        self.setReadOnly(True)

    def info(self, message: str) -> None:
        self.appendPlainText(f"[INFO] {message}")

    def error(self, message: str) -> None:
        self.appendPlainText(f"[ERROR] {message}")