from __future__ import annotations

import traceback

from PySide6.QtCore import QObject, Signal, Slot


class BaseWorker(QObject):
    """
    Базовый класс для всех фоновых задач.

    Жизненный цикл:

        started
            ↓
        execute()
            ↓
        finished

    При возникновении исключения
    генерируется сигнал error.
    """

    started = Signal()
    finished = Signal()

    log = Signal(str)

    error = Signal(str)

    # ------------------------------------------------------------------

    def __init__(self) -> None:
        super().__init__()

    # ------------------------------------------------------------------

    @Slot()
    def run(self) -> None:
        """
        Точка входа Worker.

        Запускает execute() и гарантирует
        отправку сигналов.
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
        Основная работа Worker.

        Должна быть реализована
        в наследниках.
        """

        raise NotImplementedError

    # ------------------------------------------------------------------

    def _log(
        self,
        message: str,
    ) -> None:
        """
        Отправить сообщение в журнал.
        """

        self.log.emit(message)