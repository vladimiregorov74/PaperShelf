from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Signal, Slot

from papershelf.controllers import ArticleController
from papershelf.core.exceptions import UnsupportedSiteError
from papershelf.workers.base_worker import BaseWorker


class SaveArticleWorker(BaseWorker):
    """
    Worker сохранения статьи.
    """

    success = Signal(Path)

    unsupported_site = Signal(
        str,
        object,
    )

    closed = Signal()

    # ------------------------------------------------------------------

    def __init__(self) -> None:
        super().__init__()

        self._url: str | None = None
        self._controller: ArticleController | None = None

    # ------------------------------------------------------------------

    @Slot(str)
    def save(
        self,
        url: str,
    ) -> None:
        """
        Сохранить статью.
        """

        self._log(
            f"SaveArticleWorker.save(): START url={url}"
        )

        self._url = url

        self.run()

        self._log(
            "SaveArticleWorker.save(): END"
        )

    # ------------------------------------------------------------------

    def execute(self) -> None:
        """
        Выполнить сохранение статьи.
        """

        self._log(
            "SaveArticleWorker.execute(): START"
        )

        if self._url is None:
            self._log(
                "SaveArticleWorker: URL отсутствует"
            )
            return

        controller = ArticleController()

        self._controller = controller

        self._log(
            "SaveArticleWorker: "
            f"ArticleController создан id={id(controller)}"
        )

        try:
            self._log(
                "SaveArticleWorker: "
                f"вызываем save_article(url={self._url})"
            )

            directory = controller.save_article(
                url=self._url,
                logger=self._log,
            )

            self._log(
                "SaveArticleWorker: "
                f"save_article() завершён: {directory}"
            )

            self.success.emit(
                directory,
            )

        except UnsupportedSiteError as exception:
            self._log(
                "SaveArticleWorker: "
                "получен UnsupportedSiteError"
            )

            self._log(
                f"URL={exception.url}"
            )

            self._log(
                f"page id={id(exception.page)}"
            )

            self.unsupported_site.emit(
                exception.url,
                exception.page,
            )

        finally:
            self._log(
                "SaveArticleWorker: "
                "закрываем ArticleController"
            )

            controller.close()

            self._controller = None

            self._log(
                "SaveArticleWorker: "
                "ArticleController закрыт"
            )

            self._log(
                "SaveArticleWorker.execute(): END"
            )

    # ------------------------------------------------------------------

    @Slot()
    def close(self) -> None:
        """
        Освободить ресурсы Worker.
        """

        self._log(
            "SaveArticleWorker.close(): START"
        )

        if self._controller is not None:
            self._log(
                "SaveArticleWorker.close(): "
                "закрываем текущий ArticleController"
            )

            self._controller.close()

            self._controller = None

            self._log(
                "SaveArticleWorker.close(): "
                "ArticleController закрыт"
            )

        self.closed.emit()

        self._log(
            "SaveArticleWorker.close(): END"
        )