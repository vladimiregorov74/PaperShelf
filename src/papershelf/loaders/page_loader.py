from __future__ import annotations

from abc import ABC, abstractmethod

from papershelf.models.loaded_page import LoadedPage

class PageLoader(ABC):
    """
    Базовый загрузчик веб-страниц.
    """

    @abstractmethod
    def load(
        self,
        url: str,
    ) -> LoadedPage:
        """
        Загрузить страницу.
        """