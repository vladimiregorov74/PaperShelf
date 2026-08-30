from __future__ import annotations

from PySide6.QtCore import QObject, QThread, Signal
from PySide6.QtWidgets import QMessageBox

from papershelf.config.constants import (
    STATUS_MESSAGE_LONG_TIMEOUT,
)
from papershelf.workers import SaveArticleWorker


class SaveController(QObject):
    """
    Контроллер сохранения статьи.

    Управляет Worker и QThread.
    """

    save_requested = Signal(str)

    unsupported_site = Signal(str, object,)
    
    stale_selectors = Signal(str, str, str)

    # ------------------------------------------------------------------

    def __init__(
        self,
        window,
    ) -> None:
        super().__init__()

        self._window = window

        self._worker: SaveArticleWorker | None = None
        self._thread: QThread | None = None

        self._current_url: str | None = None

    # ------------------------------------------------------------------

    def start(self) -> None:
        """
        Создать Worker и рабочий поток.
        """

        if self._thread is not None:
            return

        self._create_worker()

    # ------------------------------------------------------------------

    def _create_worker(self) -> None:
        """
        Создать Worker и его рабочий поток.
        """

        self._thread = QThread(
            self,
        )

        self._worker = SaveArticleWorker()

        self._worker.moveToThread(
            self._thread,
        )

        self._worker.log.connect(
            self._window.log_widget.info,
        )

        self._worker.success.connect(
            self._on_success,
        )

        self._worker.unsupported_site.connect(
            self._on_unsupported_site,
        )
        
        self._worker.stale_selectors.connect(
            self._on_stale_selectors,
        )
        
        self._worker.error.connect(
            self._on_error,
        )

        self.save_requested.connect(
            self._worker.save,
        )

        # --------------------------------------------------------------
        # Закрытие Worker
        # --------------------------------------------------------------

        self._worker.close_requested.connect(
            self._worker.close,
        )

        # --------------------------------------------------------------
        # Завершение Worker → завершение потока
        # --------------------------------------------------------------

        self._worker.finished.connect(
            self._thread.quit,
        )

        # --------------------------------------------------------------
        # Удаление Worker
        # --------------------------------------------------------------

        self._worker.finished.connect(
            self._worker.deleteLater,
        )

        # --------------------------------------------------------------
        # Завершение потока
        # --------------------------------------------------------------

        self._thread.finished.connect(
            self._on_thread_finished,
        )

        self._thread.start()
        
        # --------------------------------------------------------------
        # Изменение процесса скачивания
        # --------------------------------------------------------------
        
        self._worker.stage.connect(
            self._window.top_panel.set_stage,
        )

    # ------------------------------------------------------------------

    def _on_thread_finished(self) -> None:
        """
        Освободить ссылки после завершения потока.
        """

        self._worker = None
        self._thread = None

    # ------------------------------------------------------------------

    def save(
        self,
        url: str,
    ) -> None:
        """
        Начать сохранение статьи.
        """

        url = url.strip()

        if not url:
            QMessageBox.warning(
                self._window,
                "Пустой URL",
                "Введите адрес статьи.",
            )

            return

        self._current_url = url

        self._window.top_panel.set_busy(
            True,
        )

        self._window.log_widget.info(
            f"Получен URL: {url}",
        )

        self._window.status_bar.showMessage(
            "Сохранение статьи...",
        )

        if self._thread is None:
            self.start()

        self.save_requested.emit(
            url,
        )

    # ------------------------------------------------------------------

    def retry(self) -> None:
        """
        Повторить сохранение последнего URL.
        """

        if self._current_url is None:
            return

        self.save(
            self._current_url,
        )

    # ------------------------------------------------------------------

    def _on_unsupported_site(
        self,
        url: str,
        page,
    ) -> None:
        """
        Передать неподдерживаемый сайт интерфейсу.
        """

        self._window.top_panel.set_busy(
            False,
        )

        self.unsupported_site.emit(
            url,
            page,
        )

    # ------------------------------------------------------------------

    def _on_success(
        self,
        directory,
    ) -> None:
        """
        Обработать успешное сохранение.
        """

        self._window.log_widget.success(
            f"Статья успешно сохранена:\n{directory}",
        )

        self._window._reload_library()

        self._window.library_widget.select_article(
            directory,
        )

        self._window.status_bar.showMessage(
            "Статья сохранена.",
            STATUS_MESSAGE_LONG_TIMEOUT,
        )

        self._window.top_panel.set_busy(
            False,
        )

    # ------------------------------------------------------------------

    def _on_error(
        self,
        traceback_text: str,
    ) -> None:
        """
        Обработать критическую ошибку Worker.
        """

        self._window.log_widget.error(
            traceback_text,
        )

        QMessageBox.critical(
            self._window,
            "Ошибка",
            traceback_text,
        )

        self._window.status_bar.showMessage(
            "Произошла ошибка.",
            STATUS_MESSAGE_LONG_TIMEOUT,
        )

        self._window.top_panel.set_busy(
            False,
        )

    # ------------------------------------------------------------------
    
    def _on_stale_selectors(
            self,
            url: str,
            identifier: str,
            source: str,
    ) -> None:
        
        self._window.top_panel.set_busy(False)
        
        self.stale_selectors.emit(url, identifier, source)
        
    # ------------------------------------------------------------------

    def close(self) -> None:
        """
        Завершить Worker и рабочий поток.
        """

        if self._worker is None:
            return

        if self._thread is None:
            return

        self._worker.close_requested.emit()

        self._thread.quit()

        self._thread.wait()

        self._worker = None
        self._thread = None