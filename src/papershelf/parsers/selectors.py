"""
CSS-селекторы поддерживаемых сайтов.

Если сайт изменит верстку, изменения потребуется
внести только в этот файл.
"""

from __future__ import annotations

# ----------------------------------------------------------------------

# wezom.academy

# ----------------------------------------------------------------------

WEZOM_AUTHOR_SELECTORS = (
    'div.text-block__author._plr-def._mb-def',
    'a.text-block__author-link',
)

WEZOM_ARTICLE_SELECTORS = (
    'div.wysiwyg._mt-lg',
)

WEZOM_CONTENT_SELECTORS = (
    'div.wysiwyg._mt-lg',
)

WEZOM_REMOVE_SELECTORS = (
)

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

# dan-it.com.ua

# ----------------------------------------------------------------------

DAN_IT_AUTHOR_SELECTORS = (
    'meta[name="author"]',
    'div.blog-author-name-block',
    'span.blog-author-name-block__text',
    'h3.blog-author-name',
    'p.blog-author-title',
    'a.blog-author-title__link',
)

DAN_IT_ARTICLE_SELECTORS = (
    '#blog-post-content',
)

DAN_IT_CONTENT_SELECTORS = (
    '#blog-post-content',
)

DAN_IT_REMOVE_SELECTORS = (
)
