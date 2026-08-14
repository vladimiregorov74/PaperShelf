"""
CSS-селекторы поддерживаемых сайтов.

Если сайт изменит верстку, изменения потребуется
внести только в этот файл.
"""

from __future__ import annotations

# ----------------------------------------------------------------------

# habr.com

# ----------------------------------------------------------------------

HABR_AUTHOR_SELECTORS = (
    'span.tm-user-info.author',
)

HABR_ARTICLE_SELECTORS = (
    'div.article-formatted-body.article-formatted-body.article-formatted-body_version-2',
)

HABR_CONTENT_SELECTORS = (
    'div.article-formatted-body.article-formatted-body.article-formatted-body_version-2',
)

HABR_REMOVE_SELECTORS = (
)

# ----------------------------------------------------------------------

# metanit.com

# ----------------------------------------------------------------------

METANIT_AUTHOR_SELECTORS = (
)

METANIT_ARTICLE_SELECTORS = (
    'div.item.center.menC',
)

METANIT_CONTENT_SELECTORS = (
    'div.item.center.menC',
)

METANIT_REMOVE_SELECTORS = (
    'div.date',
    'div.nav',
    'div.socBlock',
    'div[id^="yandex_rtb"]',
)
