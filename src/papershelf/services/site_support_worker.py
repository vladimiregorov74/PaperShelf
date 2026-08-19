from __future__ import annotations

from PySide6.QtCore import Signal

from papershelf.services.site_support_service import SiteSupportService
from papershelf.workers.base_worker import BaseWorker


class SiteSupportWorker(BaseWorker):
    """
    Worker анализа нового сайта.
    """

    success = Signal()

    # ------------------------------------------------------------------

    def __init__(
            self,
            service: SiteSupportService,
            url: str,
            source: str,
            title_suffix: str,
    ) -> None:
        super().__init__()

        self._service = service
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

        self._service.register(
            url=self._url,
            logger=self._log,
            source=self._source,
            title_suffix=self._title_suffix,
        )

        self.success.emit()