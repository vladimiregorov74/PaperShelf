from __future__ import annotations

from papershelf.core.exceptions import UnsupportedSiteError
from papershelf.parsers.base_parser import BaseParser
from papershelf.parsers.habr_parser import HabrParser
from papershelf.parsers.metanit_parser import MetanitParser

# ------------------------------------------------------------------
# Registered parsers
# ------------------------------------------------------------------

PARSERS: tuple[type[BaseParser], ...] = (
    HabrParser,
    MetanitParser,
)


class ParserFactory:
    """
    Фабрика парсеров.

    Назначение
    ----------
    Создаёт парсер,
    подходящий для указанного URL.
    """

    # ------------------------------------------------------------------

    @classmethod
    def create(
        cls,
        url: str,
    ) -> BaseParser:

        for parser_class in PARSERS:

            if parser_class.can_parse(url):
                return parser_class()

        raise UnsupportedSiteError(url)