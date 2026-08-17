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
    ) -> None:
        super().__init__()

        self._service = service
        self._url = url

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
        )

        self.success.emit()