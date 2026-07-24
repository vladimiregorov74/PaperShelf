from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Signal

from papershelf.controllers import ArticleController
from papershelf.workers.base_worker import BaseWorker


class SaveArticleWorker(BaseWorker):
    """
    Фоновое сохранение статьи.
    """

    success = Signal(Path)

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
        
        directory = self._controller.save_article(
            url=self._url,
            logger=self._log,
        )
        
        self.success.emit(directory)