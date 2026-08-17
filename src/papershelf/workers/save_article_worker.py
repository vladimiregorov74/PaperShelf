from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Signal

from papershelf.controllers import ArticleController
from papershelf.workers.base_worker import BaseWorker
from papershelf.core.exceptions import UnsupportedSiteError


class SaveArticleWorker(BaseWorker):
    """
    Worker сохранения статьи.
    """

    success = Signal(Path)
    unsupported_site = Signal(str)

    # ------------------------------------------------------------------

    def __init__(
        self,
        controller: ArticleController,
        url: str,
    ) -> None:
        super().__init__()

        self._controller = controller
        self._url = url

    # ------------------------------------------------------------------
    
    def execute(self) -> None:
        """
        Выполнить сохранение статьи.
        """
        
        try:
            
            directory = self._controller.save_article(
                url=self._url,
                logger=self._log,
            )
        
        except UnsupportedSiteError as exc:
            
            self.unsupported_site.emit(
                exc.url,
            )
            
            return
        
        self.success.emit(
            directory,
        )