"""
CSS-селекторы поддерживаемых сайтов.

Если сайт изменит верстку, изменения потребуется
внести только в этот файл.
"""

from __future__ import annotations




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

# ----------------------------------------------------------------------

# productstar.ru

# ----------------------------------------------------------------------

PRODUCTSTAR_AUTHOR_SELECTORS = (
)

PRODUCTSTAR_ARTICLE_SELECTORS = (
    'div.blog-post-page__content',
)

PRODUCTSTAR_CONTENT_SELECTORS = (
    'div.blog-post-page__content',
)

PRODUCTSTAR_REMOVE_SELECTORS = (
)

# ----------------------------------------------------------------------

# habr.com

# ----------------------------------------------------------------------

HABR_AUTHOR_SELECTORS = (
    'span.tm-user-info.author',
    'div.article-author',
)

HABR_ARTICLE_SELECTORS = (
    'div.article-formatted-body.article-formatted-body.article-formatted-body_version-1',
)

HABR_CONTENT_SELECTORS = (
    'div.article-formatted-body.article-formatted-body.article-formatted-body_version-1',
)

HABR_REMOVE_SELECTORS = (
    'a',
)
