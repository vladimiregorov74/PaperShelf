from __future__ import annotations

from abc import ABC
from abc import abstractmethod


class PageLoader(ABC):
    """
    Базовый загрузчик HTML-страниц.
    """

    # ------------------------------------------------------------------

    @abstractmethod
    def load(
        self,
        url: str,
    ) -> str:
        """
        Загрузить HTML страницы.
        """