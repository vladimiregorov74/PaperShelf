"""
Сборка SiteConfig для GenericParser/ParserFactory.
"""

from __future__ import annotations

import importlib

from papershelf.parsers.generic_parser import SiteConfig


# ----------------------------------------------------------------------


def _build_config(
    selectors_module,
    prefix: str,
    domain: str,
    source: str,
    title_suffix: str,
) -> SiteConfig:
    """
    Собрать SiteConfig, подставив кортежи селекторов из selectors.py.
    """

    def _get(
        suffix: str,
    ) -> tuple[str, ...]:
        return getattr(
            selectors_module,
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


# ----------------------------------------------------------------------


def get_site_configs() -> tuple[SiteConfig, ...]:
    """
    Получить актуальный список конфигураций сайтов.

    Перед построением конфигураций выполняется повторная загрузка
    modules selectors.py и site_registry_data.py, благодаря чему
    приложение сразу видит новые сайты после работы SiteInspector
    без необходимости перезапуска.
    """

    selectors = importlib.import_module(
        "papershelf.parsers.selectors",
    )

    site_registry_data = importlib.import_module(
        "papershelf.parsers.site_registry_data",
    )

    selectors = importlib.reload(
        selectors,
    )

    site_registry_data = importlib.reload(
        site_registry_data,
    )

    return tuple(
        _build_config(
            selectors,
            *site,
        )
        for site in site_registry_data._SITES
    )