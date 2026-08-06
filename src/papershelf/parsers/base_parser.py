from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from papershelf.models import Article


class BaseParser(ABC):
    """
    Базовый класс для всех парсеров.
    """

    # ------------------------------------------------------------------

    @classmethod
    @abstractmethod
    def can_parse(
        cls,
        url: str,
    ) -> bool:
        """
        Проверить, поддерживает ли парсер указанный URL.

        Parameters
        ----------
        url:
            Адрес страницы.

        Returns
        -------
        bool
            True, если парсер поддерживает URL.
        """

        raise NotImplementedError

    # ------------------------------------------------------------------

    @abstractmethod
    def parse(
        self,
        html: str,
        url: str,
    ) -> Article:
        """
        Преобразовать HTML страницы в объект Article.

        Parameters
        ----------
        html:
            HTML страницы.

        url:
            Адрес страницы.

        Returns
        -------
        Article
        """

        raise NotImplementedError