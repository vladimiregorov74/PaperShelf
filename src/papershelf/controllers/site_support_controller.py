from __future__ import annotations

from PySide6.QtCore import QObject, QThread, Signal

from papershelf.services.site_support_worker import SiteSupportWorker


class SiteSupportController(QObject):
    """
    Контроллер регистрации нового сайта.
    """

    completed = Signal()

    error = Signal(str)

    exception = Signal(object)

    # ------------------------------------------------------------------

    def __init__(
        self,
        parent=None,
    ) -> None:
        super().__init__(parent)

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

        if self._thread is not None:
            return

        self._thread = QThread(
            self,
        )

        self._worker = SiteSupportWorker(
            url=url,
            source=source,
            title_suffix=title_suffix,
        )

        self._worker.moveToThread(
            self._thread,
        )

        # --------------------------------------------------------------
        # Лог
        # --------------------------------------------------------------

        self._worker.log.connect(
            logger,
        )

        # --------------------------------------------------------------
        # Результат
        # --------------------------------------------------------------

        self._worker.success.connect(
            self.completed.emit,
        )

        self._worker.exception.connect(
            self._on_exception,
        )

        self._worker.error.connect(
            self.error.emit,
        )

        # --------------------------------------------------------------
        # Завершение обычной работы
        # --------------------------------------------------------------

        self._worker.finished.connect(
            self._thread.quit,
        )

        self._worker.finished.connect(
            self._worker.deleteLater,
        )

        # --------------------------------------------------------------
        # Закрытие Worker
        # --------------------------------------------------------------

        self._worker.closed.connect(
            self._on_worker_closed,
        )

        # --------------------------------------------------------------
        # Завершение потока
        # --------------------------------------------------------------

        self._thread.finished.connect(
            self._cleanup,
        )
        self._thread.finished.connect(
	        lambda: print("THREAD FINISHED", id(self._thread))
        )

        # --------------------------------------------------------------
        # Запуск
        # --------------------------------------------------------------

        self._thread.started.connect(
            self._worker.run,
        )

        self._thread.start()

    # ------------------------------------------------------------------

    def _on_exception(
        self,
        exception: Exception,
    ) -> None:
        """
        Передать специальное исключение интерфейсу.
        """

        self.exception.emit(
            exception,
        )

    # ------------------------------------------------------------------

    def _on_worker_closed(
        self,
    ) -> None:
        """
        Завершить поток после освобождения ресурсов Worker.
        """

        if self._thread is None:
            return

        self._thread.quit()

    # ------------------------------------------------------------------

    def _cleanup(
        self,
    ) -> None:
        """
        Очистить ссылки после завершения потока.
        """
        print("CLEANUP", id(self))
        self._worker = None
        self._thread = None

    # ------------------------------------------------------------------

    def close(
        self,
    ) -> None:
        """
        Запросить закрытие Worker.
        """

        if self._worker is None:
            return

        self._worker.close_requested.emit()