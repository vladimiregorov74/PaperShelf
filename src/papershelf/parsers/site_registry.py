"""
Сборка SiteConfig для GenericParser/ParserFactory.

Этот файл — стабильный, его можно и нужно дорабатывать руками при
необходимости (например, поменять правило сборки source/title_suffix).
tools/inspect_site.py его НЕ переписывает — он пишет только чистые
данные в site_registry_data.py (_SITES), которые этот файл импортирует.
"""

from __future__ import annotations

from papershelf.parsers import selectors as _selectors
from papershelf.parsers.generic_parser import SiteConfig
from papershelf.parsers.site_registry_data import _SITES


def _build_config(
    prefix: str,
    domain: str,
    source: str,
    title_suffix: str,
) -> SiteConfig:
    """
    Собрать SiteConfig, подставив кортежи селекторов из selectors.py
    по префиксу (METANIT_ARTICLE_SELECTORS, METANIT_CONTENT_SELECTORS
    и т.д.). Если для сайта какой-то кортеж не определён — используется
    пустой кортеж.
    """

    def _get(suffix: str) -> tuple[str, ...]:
        return getattr(
            _selectors,
            f"{prefix}_{suffix}",
            (),
        )

    return SiteConfig(
        domain=domain,
        source=source,
        article_selectors=_get("ARTICLE_SELECTORS"),
        content_selectors=_get("CONTENT_SELECTORS"),
        remove_selectors=_get("REMOVE_SELECTORS"),
        author_selectors=_get("AUTHOR_SELECTORS"),
        title_suffix=title_suffix,
    )


SITE_CONFIGS: tuple[SiteConfig, ...] = tuple(
    _build_config(*site) for site in _SITES
)
