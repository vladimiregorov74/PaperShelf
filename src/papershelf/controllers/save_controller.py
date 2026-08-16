from __future__ import annotations

from PySide6.QtCore import QThread
from PySide6.QtWidgets import QMessageBox

from papershelf.config.constants import STATUS_MESSAGE_LONG_TIMEOUT, STATUS_MESSAGE_TIMEOUT
from papershelf.controllers.article_controller import ArticleController
from papershelf.workers import SaveArticleWorker


class SaveController:
    """
    Контроллер сохранения статьи.

    Полностью управляет Worker и QThread.
    """

    # ------------------------------------------------------------

    def __init__(
        self,
        window,
        controller: ArticleController,
    ) -> None:

        self._window = window
        self._controller = controller

        self._worker: SaveArticleWorker | None = None
        self._thread: QThread | None = None

    # ------------------------------------------------------------

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

        self._window.top_panel.set_busy(True)

        self._window.log_widget.info(
            f"Получен URL: {url}"
        )

        self._window.status_bar.showMessage(
            "Сохранение статьи..."
        )

        self._thread = QThread(
            self._window
        )

        self._worker = SaveArticleWorker(
            controller=self._controller,
            url=url,
        )

        self._worker.moveToThread(
            self._thread
        )

        #
        # запуск
        #

        self._thread.started.connect(
            self._worker.run
        )

        #
        # лог
        #

        self._worker.log.connect(
            self._window.log_widget.info
        )

        #
        # события
        #

        self._worker.success.connect(
            self._on_success
        )

        self._worker.error.connect(
            self._on_error
        )

        self._worker.finished.connect(
            self._on_finished
        )

        #
        # закрытие
        #

        self._worker.finished.connect(
            self._thread.quit
        )

        self._worker.finished.connect(
            self._worker.deleteLater
        )

        self._thread.finished.connect(
            self._thread.deleteLater
        )

        self._thread.start()

    # ------------------------------------------------------------

    def _on_success(
        self,
        directory,
    ) -> None:
        """
        Статья успешно сохранена.
        """

        self._window.log_widget.success(
            f"Статья успешно сохранена:\n{directory}"
        )

        self._window._reload_library()

        self._window.library_widget.select_article(
            directory
        )

        self._window.status_bar.showMessage(
            "Статья сохранена.",
            STATUS_MESSAGE_LONG_TIMEOUT,
        )

    # ------------------------------------------------------------

    def _on_error(
        self,
        traceback_text: str,
    ) -> None:
        """
        Ошибка.
        """

        self._window.log_widget.error(
            traceback_text
        )

        QMessageBox.critical(
            self._window,
            "Ошибка",
            traceback_text,
        )

        self._window.status_bar.showMessage(
            "Ошибка сохранения.",
            STATUS_MESSAGE_LONG_TIMEOUT,
        )

    # ------------------------------------------------------------

    def _on_finished(
        self,
    ) -> None:
        """
        Завершение Worker.
        """

        self._window.top_panel.set_busy(
            False
        )

        self._window.status_bar.showMessage(
            "Готово.",
            STATUS_MESSAGE_TIMEOUT,
        )

        self._worker = None
        self._thread = None