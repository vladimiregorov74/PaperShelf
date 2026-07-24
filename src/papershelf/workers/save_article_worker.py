from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Signal

from papershelf.controllers import ArticleController
from papershelf.workers.base_worker import BaseWorker

class SaveArticleWorker(BaseWorker):
    """
    Worker сохранения статьи.

    Выполняет полный цикл:

        Загрузка страницы
            ↓
        Парсинг
            ↓
        Экспорт
            ↓
        Сохранение

    После успешного завершения
    отправляет путь к созданной папке.
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
        """
        Выполнить сохранение статьи.
        """
        
        directory = self._controller.save_article(
            url=self._url,
            logger=self._log,
        )
        
        self.success.emit(directory)