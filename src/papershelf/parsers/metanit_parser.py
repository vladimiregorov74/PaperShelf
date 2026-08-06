from papershelf.parsers import BaseParser


class MetanitParser(BaseParser):

    ARTICLE_SELECTOR = (
        "div.article-body",
    )

    TITLE_SELECTOR = (
        "h1",
    )

    AUTHOR_SELECTOR = ()

    DATE_SELECTOR = ()