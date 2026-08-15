from __future__ import annotations

from papershelf.core.exceptions import UnsupportedSiteError
from papershelf.parsers.base_parser import BaseParser
from papershelf.parsers.generic_parser import GenericParser
from papershelf.parsers.site_registry import SITE_CONFIGS


class ParserFactory:
    """
    Фабрика парсеров.

    Назначение
    ----------
    Создаёт GenericParser, настроенный под URL, вместо выбора между
    заранее написанными классами-парсерами по одному на сайт.
    """

    # ------------------------------------------------------------------

    @classmethod
    def create(
        cls,
        url: str,
    ) -> BaseParser:

        for config in SITE_CONFIGS:

            parser = GenericParser(config)
            print(parser.can_parse(url), url)

            if parser.can_parse(url):
                return parser

        raise UnsupportedSiteError(url)
