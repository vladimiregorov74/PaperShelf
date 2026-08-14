from __future__ import annotations

from papershelf.parsers import selectors as _selectors
from papershelf.parsers.generic_parser import SiteConfig

# ------------------------------------------------------------------
# Единственное, что реально нужно писать руками на новый сайт — вот
# эти 4 поля на строку. Сами кортежи селекторов (ARTICLE/CONTENT/
# REMOVE/AUTHOR) подтягиваются из selectors.py по префиксу автоматически
# в _build_config — их отдельно перечислять здесь не нужно.
#
# (префикс_в_selectors.py, домен_для_can_parse, отображаемое_имя_source, суффикс_заголовка)
# ------------------------------------------------------------------

_SITES: tuple[tuple[str, str, str, str], ...] = (
    ("METANIT", "metanit.com", "Metanit", ""),
    ("HABR", "habr.com", "Habr", " / Хабр"),
    ("DAN_IT", "dan-it.com.ua", "DAN IT Education", ""),
)


def _build_config(
    prefix: str,
    domain: str,
    source: str,
    title_suffix: str,
) -> SiteConfig:
    """
    Собрать SiteConfig, подставив кортежи селекторов из selectors.py
    по префиксу (METANIT_ARTICLE_SELECTORS, METANIT_CONTENT_SELECTORS
    и т.д.). Если для сайта какой-то кортеж не определён (например
    AUTHOR_SELECTORS у metanit.com пустой) — используется ().
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
