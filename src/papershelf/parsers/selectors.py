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

# www.eurointegration.com.ua

# ----------------------------------------------------------------------

WWW_AUTHOR_SELECTORS = (
    'span.post__author',
    'div.article__author',
)

WWW_ARTICLE_SELECTORS = (
    'div.post__text',
)

WWW_CONTENT_SELECTORS = (
    'div.post__text',
)

WWW_REMOVE_SELECTORS = (
    'div.mobile-only-ads',
    'ins[class*="adsbygoogle"]',
)

# ----------------------------------------------------------------------

# epravda.com.ua

# ----------------------------------------------------------------------

EPRAVDA_AUTHOR_SELECTORS = (
    'span.post_news_author',
)

EPRAVDA_ARTICLE_SELECTORS = (
    'div.post_article_text',
)

EPRAVDA_CONTENT_SELECTORS = (
    'div.post_article_text',
)

EPRAVDA_REMOVE_SELECTORS = (
    'div.also_box',
)

# ----------------------------------------------------------------------

# life.pravda.com.ua

# ----------------------------------------------------------------------

LIFE_AUTHOR_SELECTORS = (
    'span.post_news_author',
)

LIFE_ARTICLE_SELECTORS = (
    'div.post_article_text',
)

LIFE_CONTENT_SELECTORS = (
    'div.post_article_text',
)

LIFE_REMOVE_SELECTORS = (
    'div.also_box',
)

# ----------------------------------------------------------------------

# habr.com

# ----------------------------------------------------------------------

HABR_AUTHOR_SELECTORS = (
    'span.tm-user-info.author',
    'div.article-author',
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
