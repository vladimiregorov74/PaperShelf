from __future__ import annotations

import re

from bs4 import Tag

# ------------------------------------------------------------------
# Единая точка построения CSS-селекторов. Раньше был скопирован в трёх
# местах (container_analyzer.py, article_author_detector.py,
# inspector.py) без фильтрации JS-хуков и без экранирования спецсимволов
# в классах — теперь один источник истины для всех трёх.
# ------------------------------------------------------------------

# Служебные классы-хуки для JS-поведения (не про вёрстку/стили) —
# менее стабильны, чем семантические/стилевые классы: могут исчезнуть
# при рефакторинге фронтенда, даже если внешний вид не поменяется.
_SKIP_CLASS_PREFIXES = ("js-", "is-", "has-")

_VALID_CSS_IDENT = re.compile(r"^-?[A-Za-z_][A-Za-z0-9_-]*$")


def _is_valid_css_ident(value: str) -> bool:
    """
    Проверяет, что строку можно безопасно использовать как CSS-класс/id
    без экранирования (буквы/цифры/дефис/подчёркивание, не начинается
    с цифры).
    """

    return bool(
        _VALID_CSS_IDENT.match(
            value,
        )
    )


def build_selector(
    tag: Tag,
) -> str:
    """
    Построить устойчивый CSS-селектор элемента: id -> тег + все
    содержательные классы (кроме служебных JS-хуков) -> просто тег.

    Если значение id/класса содержит символы, недопустимые в CSS-
    идентификаторе без экранирования (например ':', ';', как в старой
    разметке SyntaxHighlighter: class="brush:py;"), используется
    атрибутный селектор вместо '#id'/'.class' — иначе получился бы
    невалидный (или неверно интерпретируемый) селектор.

    Parameters
    ----------
    tag:
        HTML-элемент BeautifulSoup.

    Returns
    -------
    str
    """

    css_id = tag.get("id")

    if css_id:
        if _is_valid_css_ident(css_id):
            return f"#{css_id}"
        return f'{tag.name}[id="{css_id}"]'

    css_classes = tag.get("class", []) or []

    useful = [
        css_class
        for css_class in css_classes
        if not css_class.startswith(_SKIP_CLASS_PREFIXES)
    ]

    if not useful:
        return tag.name

    if all(_is_valid_css_ident(c) for c in useful):
        return tag.name + "".join(f".{c}" for c in useful)

    safe = useful[0].replace('"', '\\"')

    return f'{tag.name}[class~="{safe}"]'
