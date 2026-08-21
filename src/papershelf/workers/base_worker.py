from __future__ import annotations

import traceback

from PySide6.QtCore import QObject, Signal, Slot

from papershelf.core.exceptions import UnsupportedSiteError

from papershelf.core.exceptions import PaperShelfError

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
    отправляет само исключение и traceback.
    """

    started = Signal()
    finished = Signal()

    log = Signal(str)

    #
    # Полный traceback.
    #
    error = Signal(str)

    #
    # Сам объект исключения.
    #
    exception = Signal(object)

    # ------------------------------------------------------------------

    def __init__(self) -> None:
        super().__init__()

    # ------------------------------------------------------------------
    
    @Slot()
    def run(self) -> None:
        """
        Точка входа Worker.
        """
        
        self.started.emit()
        
        try:
            self.execute()
        
        except PaperShelfError as exception:
            print("run except", type(exception).__name__)
            self.exception.emit(
                exception,
            )
            #
            # Traceback только для неожиданных ошибок.
            #
            if not isinstance(exception, PaperShelfError):
                self.error.emit(
                    traceback.format_exc(),
                )
        
        except Exception as exception:
            print("BaseWorker поймал:", type(exception).__name__)
            
            self.error.emit(
                traceback.format_exc(),
            )
        
        finally:
            print("run finally")
            self.finished.emit()

    # ------------------------------------------------------------------

    def execute(self) -> None:
        """
        Основная работа Worker.
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