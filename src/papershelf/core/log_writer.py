from __future__ import annotations

from pathlib import Path


class LogWriter:
    """
    Запись сообщений журнала в файл.
    """

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def __init__(
        self,
        log_file: Path,
    ) -> None:
        self._log_file = log_file
        self._enabled = False

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def enabled(self) -> bool:
        """
        Возвращает состояние записи в файл.
        """

        return self._enabled

    # ------------------------------------------------------------------
    # Public
    # ------------------------------------------------------------------

    def set_enabled(
        self,
        enabled: bool,
    ) -> None:
        """
        Включить или отключить запись журнала.

        Parameters
        ----------
        enabled:
            Новое состояние записи.
        """

        self._enabled = enabled

    # ------------------------------------------------------------------

    def write(
        self,
        message: str,
    ) -> None:
        """
        Записать сообщение в журнал.

        Parameters
        ----------
        message:
            Строка журнала.
        """

        if not self._enabled:
            return

        self._ensure_directory()

        with self._log_file.open(
            mode="a",
            encoding="utf-8",
        ) as file:
            file.write(message)
            file.write("\n")

    # ------------------------------------------------------------------
    # Private
    # ------------------------------------------------------------------

    def _ensure_directory(self) -> None:
        """
        Создать каталог журнала при необходимости.
        """

        self._log_file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )