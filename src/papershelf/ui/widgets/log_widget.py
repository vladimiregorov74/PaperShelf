from __future__ import annotations

from datetime import datetime

from PySide6.QtWidgets import QPlainTextEdit


class LogWidget(QPlainTextEdit):
    """
    Журнал приложения.
    """

    def __init__(self) -> None:
        super().__init__()

        self._configure()

    # ------------------------------------------------------------------

    def _configure(self) -> None:
        self.setReadOnly(True)

    # ------------------------------------------------------------------

    def _timestamp(self) -> str:
        """
        Текущее время.
        """

        return datetime.now().strftime("%H:%M:%S")

    # ------------------------------------------------------------------

    def _write(
        self,
        level: str,
        message: str,
    ) -> None:
        """
        Добавить запись в журнал.
        """

        self.appendPlainText(
            f"[{self._timestamp()}] {level:<7} {message}"
        )

    # ------------------------------------------------------------------

    def info(
        self,
        message: str,
    ) -> None:
        self._write("INFO", message)

    # ------------------------------------------------------------------

    def success(
        self,
        message: str,
    ) -> None:
        self._write("SUCCESS", message)

    # ------------------------------------------------------------------

    def warning(
        self,
        message: str,
    ) -> None:
        self._write("WARNING", message)

    # ------------------------------------------------------------------

    def error(
        self,
        message: str,
    ) -> None:
        self._write("ERROR", message)

    # ------------------------------------------------------------------

    def clear_log(self) -> None:
        """
        Очистить журнал.
        """

        self.clear()