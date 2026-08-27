from __future__ import annotations

import traceback

from PySide6.QtCore import QObject, Signal, Slot

from papershelf.core.exceptions import PaperShelfError


class BaseWorker(QObject):
    """
    Базовый класс для фоновых задач.
    """

    started = Signal()
    finished = Signal()

    log = Signal(str)

    error = Signal(str)
    exception = Signal(object)
    
    close_requested = Signal()

    # ------------------------------------------------------------------

    def __init__(self) -> None:
        super().__init__()

    # ------------------------------------------------------------------
    
    @Slot()
    def run(self) -> None:
        """
        Точка входа Worker.
        """

        self._log(
            f"{self.__class__.__name__}: run() START"
        )
        
        self.started.emit()
        
        try:
            self._log(
                f"{self.__class__.__name__}: execute() START"
            )
            
            self.execute()
            
            self._log(
                f"{self.__class__.__name__}: execute() END"
            )
        
        except PaperShelfError as exception:
            self._log(
                f"{self.__class__.__name__}: "
                f"PaperShelfError: {exception!r}"
            )
            
            self.exception.emit(
                exception,
            )
        
        except Exception:
            self._log(
                f"{self.__class__.__name__}: "
                "UNHANDLED EXCEPTION"
            )
            
            self.error.emit(
                traceback.format_exc(),
            )
        
        finally:
            self._log(
                f"{self.__class__.__name__}: "
                "finished.emit()"
            )

            self.finished.emit()
            
            self._log(
                f"{self.__class__.__name__}: run() END"
            )

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