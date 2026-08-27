from __future__ import annotations

from PySide6.QtCore import Signal

from papershelf.services.site_support_service import SiteSupportService
from papershelf.workers.base_worker import BaseWorker


class SiteSupportWorker(BaseWorker):
    """
    Worker анализа нового сайта.
    """

    success = Signal()

    closed = Signal()

    # ------------------------------------------------------------------

    def __init__(
        self,
        url: str,
        source: str,
        title_suffix: str,
    ) -> None:
        super().__init__()

        self._service: SiteSupportService | None = None

        self._url = url
        self._source = source
        self._title_suffix = title_suffix

    # ------------------------------------------------------------------

    def execute(
        self,
    ) -> None:
        """
        Выполнить анализ сайта.
        """

        if self._service is None:
            self._service = SiteSupportService()

        self._service.register(
            url=self._url,
            logger=self._log,
            source=self._source,
            title_suffix=self._title_suffix,
        )

        self.success.emit()

    # ------------------------------------------------------------------

    def close(
        self,
    ) -> None:
        """
        Освободить ресурсы Worker.
        """

        if self._service is None:
            self.closed.emit()
            return

        self._service.close()

        self._service = None

        self.closed.emit()