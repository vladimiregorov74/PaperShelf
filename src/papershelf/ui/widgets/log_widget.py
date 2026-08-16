from __future__ import annotations

from papershelf.core.log_writer import LogWriter
from papershelf.core.paths import LOG_FILE
from PySide6.QtWidgets import QPlainTextEdit

from datetime import datetime


class LogWidget(QPlainTextEdit):
    """
    Журнал приложения.
    """

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def __init__(self) -> None:
        super().__init__()

        self._log_writer = LogWriter(LOG_FILE)

        self._configure()

    # ------------------------------------------------------------------
    # Configuration
    # ------------------------------------------------------------------

    def _configure(self) -> None:
        """
        Настроить виджет.
        """

        self.setReadOnly(True)

    # ------------------------------------------------------------------
    # Public
    # ------------------------------------------------------------------

    def set_file_logging(
        self,
        enabled: bool,
    ) -> None:
        """
        Включить или отключить запись журнала в файл.

        Parameters
        ----------
        enabled:
            Новое состояние логирования.
        """

        self._log_writer.set_enabled(enabled)

    # ------------------------------------------------------------------

    def clear_log(self) -> None:
        """
        Очистить журнал.
        """

        self.clear()
        self._log_writer.clear()

    # ------------------------------------------------------------------
    # Private
    # ------------------------------------------------------------------

    def _timestamp(self) -> str:
        """
        Вернуть текущее время.
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

        Parameters
        ----------
        level:
            Уровень сообщения.

        message:
            Текст сообщения.
        """

        text = (
            f"[{self._timestamp()}] "
            f"{level:<7} "
            f"{message}"
        )

        self.appendPlainText(text)

        self._log_writer.write(text)

    # ------------------------------------------------------------------
    # Logging
    # ------------------------------------------------------------------

    def info(
        self,
        message: str,
    ) -> None:
        """
        Добавить информационное сообщение.
        """

        self._write(
            "INFO",
            message,
        )

    # ------------------------------------------------------------------

    def success(
        self,
        message: str,
    ) -> None:
        """
        Добавить сообщение об успешном выполнении.
        """

        self._write(
            "SUCCESS",
            message,
        )

    # ------------------------------------------------------------------

    def warning(
        self,
        message: str,
    ) -> None:
        """
        Добавить предупреждение.
        """

        self._write(
            "WARNING",
            message,
        )

    # ------------------------------------------------------------------

    def error(
        self,
        message: str,
    ) -> None:
        """
        Добавить сообщение об ошибке.
        """

        self._write(
            "ERROR",
            message,
        )