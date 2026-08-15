"""
CSS-селекторы поддерживаемых сайтов.

Если сайт изменит верстку, изменения потребуется
внести только в этот файл.

ARTICLE_SELECTORS отвечает на вопрос:

«Где находится статья?»

А CONTENT_SELECTORS:

«Какая часть найденной статьи является собственно содержимым, которое нужно сохранить?»
"""

from __future__ import annotations

# ----------------------------------------------------------------------
# Habr
# ----------------------------------------------------------------------

HABR_AUTHOR_SELECTORS = (
    "a.tm-user-info__username",
    "span.tm-user-info__username",
    "a[class*='user-info']",
    "meta[name='author']",
)

HABR_ARTICLE_SELECTORS = (
    "article.tm-article-presenter__content",
    "div.tm-article-presenter__content",
    "article",
)

HABR_CONTENT_SELECTORS = (
    "div.tm-article-body",
    "div.article-formatted-body",
    "div.tm-article-body__content",
)



# ----------------------------------------------------------------------

# metanit.com

# ----------------------------------------------------------------------

METANIT_AUTHOR_SELECTORS = (
)

METANIT_ARTICLE_SELECTORS = (
    "div.item.center.menC",
)

METANIT_CONTENT_SELECTORS = (
    "div.item.center.menC",
)

METANIT_REMOVE_SELECTORS = (
    "div.date",
    "div.nav",
    "div.socBlock",
    'div[id^="yandex_rtb"]',
)

# ----------------------------------------------------------------------

# dan-it.com.ua

# ----------------------------------------------------------------------

DAN_IT_AUTHOR_SELECTORS = (
    "meta[name='author']",
    "div.blog-author-name-block",
    "span.blog-author-name-block__text",
    "h3.blog-author-name",
    "p.blog-author-title",
    "a.blog-author-title__link",
)

DAN_IT_ARTICLE_SELECTORS = (
    "main#blog-post-content.blog-main-content",
)

DAN_IT_CONTENT_SELECTORS = (
    "main#blog-post-content.blog-main-content",
)

DAN_IT_REMOVE_SELECTORS = (
)
