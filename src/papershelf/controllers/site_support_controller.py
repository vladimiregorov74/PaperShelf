from __future__ import annotations

from PySide6.QtCore import QObject, QThread, Signal

from papershelf.services.site_support_service import SiteSupportService
from papershelf.services.site_support_worker import SiteSupportWorker


class SiteSupportController(QObject):
    """
    Контроллер регистрации нового сайта.
    """

    completed = Signal()
    error = Signal(str)
    exception = Signal(Exception)
    
    # ------------------------------------------------------------------
    
    def __init__(
            self,
            service: SiteSupportService,
            parent=None,
    ) -> None:
        super().__init__(parent)
        
        self._service = service
        
        self._thread: QThread | None = None
        self._worker: SiteSupportWorker | None = None

    # ------------------------------------------------------------------

    def register(
		    self,
		    url: str,
		    logger,
		    source: str,
		    title_suffix: str,
    ) -> None:
        """
        Начать регистрацию нового сайта.
        """

        self._thread = QThread()
        
        self._worker = SiteSupportWorker(
	        service=self._service,
	        url=url,
	        source=source,
	        title_suffix=title_suffix,
        )
        self._worker.moveToThread(
            self._thread,
        )

        #
        # запуск
        #

        self._thread.started.connect(
            self._worker.run,
        )

        #
        # лог
        #

        self._worker.log.connect(
            logger,
        )

        #
        # события
        #

        self._worker.success.connect(
            self.completed.emit,
        )
        
        self._worker.exception.connect(
            self._on_exception,
        )
        
        self._worker.error.connect(
            self.error.emit,
        )

        #
        # очистка
        #

        self._worker.finished.connect(
            self._thread.quit,
        )

        self._worker.finished.connect(
            self._worker.deleteLater,
        )

        self._thread.finished.connect(
            self._thread.deleteLater,
        )

        self._thread.finished.connect(
            self._cleanup,
        )
        
        self._thread.start()

    # ------------------------------------------------------------------

    def _cleanup(
        self,
    ) -> None:

        self._worker = None
        self._thread = None
    
    # ------------------------------------------------------------------
    
    def _on_exception(
            self,
            exception: Exception,
    ) -> None:
        """
        Передать специальное исключение
        в интерфейс.
        """
        
        self.exception.emit(
            exception,
        )