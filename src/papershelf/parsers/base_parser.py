from __future__ import annotations

from abc import ABC, abstractmethod

from papershelf.models import Article


class BaseParser(ABC):
    """
    Базовый класс для всех парсеров.
    """

    @abstractmethod
    def parse(
        self,
        html: str,
        url: str,
    ) -> Article:
        """
        Преобразовать HTML страницы в объект Article.
        """
        raise NotImplementedError