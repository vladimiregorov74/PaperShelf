from __future__ import annotations

import traceback

from PySide6.QtCore import QObject
from PySide6.QtCore import Signal
from PySide6.QtCore import Slot


class BaseWorker(QObject):
    """
    Базовый класс для всех фоновых задач.
    """

    started = Signal()
    finished = Signal()
    error = Signal(str)

    log = Signal(str)

    # ------------------------------------------------------------------

    @Slot()
    def run(self) -> None:
        """
        Запустить задачу.

        Не переопределяется.
        """

        self.started.emit()

        try:

            self.execute()

        except Exception:

            self.error.emit(
                traceback.format_exc()
            )

        finally:

            self.finished.emit()

    # ------------------------------------------------------------------

    def execute(self) -> None:
        """
        Основная логика.

        Должна быть реализована
        в наследнике.
        """

        raise NotImplementedError
    
   # ------------------------------------------------------------------

    def _log(
        self,
        message: str,
    ) -> None:
        """
        Отправить сообщение в лог.
        """

        self.log.emit(message)