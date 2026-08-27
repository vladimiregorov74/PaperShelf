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

# massonnn.notion.site

# ----------------------------------------------------------------------

MASSONNN_AUTHOR_SELECTORS = (
    'meta[property="article:author"]',
)

MASSONNN_ARTICLE_SELECTORS = (
    'div.notion-page-content',
)

MASSONNN_CONTENT_SELECTORS = (
    'div.notion-page-content',
)

MASSONNN_REMOVE_SELECTORS = (
    'div.notion-selectable.notion-page-block',
)
