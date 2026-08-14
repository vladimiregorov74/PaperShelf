#!/usr/bin/env python3
"""
detector.py — универсальный детектор селекторов html-страницы со статьёй.

Идея работы:
  1. Из DOM вырезаются <script>/<style>/<noscript>/комментарии и явные
     шапка/подвал/навигация (<header>/<footer>/<nav>/<aside>,
     role=banner|navigation|contentinfo).
  2. Среди оставшихся контейнеров считается "текстовый скор" (в духе
     алгоритма Arc90 Readability): суммарная длина текста в <p> внутри
     контейнера минус штраф за высокую плотность ссылок. Контейнер с
     максимальным скором — кандидат в тело статьи (ARTICLE_SELECTORS).
  3. Внутри тела статьи ищутся:
       - блок автора (meta/rel=author/itemprop=author/классы author|byline)
         -> AUTHOR_SELECTORS
       - реальные текстовые узлы (p, h2-h4, blockquote, li) -> CONTENT_SELECTORS
       - "мусорные" узлы (реклама/баннеры/шеринг/related/comments) по словарю
         ключевых слов в class/id, тегам iframe/ins, и по плотности ссылок
         -> REMOVE_SELECTORS
  4. Если передано НЕСКОЛЬКО страниц одного сайта — селекторы валидируются
     голосованием: селектор попадает в финальный набор, только если он
     сработал на достаточной доле страниц. Это сильно повышает точность,
     особенно для REMOVE_SELECTORS (баннеры/шаринг обычно на каждой
     странице сайта в одном и том же месте DOM).

Использование:
  python detector.py --site ntv --out selectors.py page1.html page2.html ...
  python detector.py --site ntv --out selectors.py --url https://example.com/article1 https://example.com/article2
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from dataclasses import dataclass, field

from bs4 import BeautifulSoup, Comment, Tag

# --------------------------------------------------------------------------
# Словари эвристик
# --------------------------------------------------------------------------

NOISE_KEYWORDS = [
    "advert", "banner", "sponsor", "promo", "subscribe", "subscription",
    "newsletter", "share", "social", "sharing", "socbtn", "soc-button",
    "related", "recommend", "recirculation", "also-read", "read-more",
    "comment", "disqus", "widget", "popup", "modal", "cookie", "paywall",
    "taboola", "outbrain", "yandex-direct", "adsbygoogle", "ad-slot",
    "ad-container", "teaser", "breadcrumbs", "tags-list", "rating",
    "print-btn", "toolbar", "floating", "sticky-share", "vk-share",
    "telegram-share", "whatsapp-share",
]

AUTHOR_KEYWORDS = ["author", "byline", "writer", "journalist", "columnist"]

STRUCTURAL_SKIP_TAGS = {"header", "footer", "nav", "aside", "form", "iframe",
                         "script", "style", "noscript", "template"}
STRUCTURAL_SKIP_ROLES = {"banner", "navigation", "contentinfo", "complementary"}

CONTENT_TAGS = ["p", "h2", "h3", "h4", "blockquote", "li", "pre"]
CONTAINER_TAGS = ["article", "main", "div", "section"]

MIN_PARAGRAPH_LEN = 40   # символов, чтобы <p> считался "содержательным"
MIN_ARTICLE_SCORE = 120  # минимальный скор контейнера, чтобы считать его статьёй


# --------------------------------------------------------------------------
# Вспомогательные функции
# --------------------------------------------------------------------------

def clean_soup(soup: BeautifulSoup) -> None:
    """Удаляет script/style/noscript/comments прямо в DOM (in-place)."""
    for tag in soup(["script", "style", "noscript", "template"]):
        tag.decompose()
    for c in soup.find_all(string=lambda s: isinstance(s, Comment)):
        c.extract()


def is_structural_chrome(tag: Tag) -> bool:
    """True, если элемент — явно шапка/подвал/навигация/боковая панель."""
    if tag.name in STRUCTURAL_SKIP_TAGS:
        return True
    role = (tag.get("role") or "").lower()
    if role in STRUCTURAL_SKIP_ROLES:
        return True
    return False


def text_len(tag: Tag) -> int:
    return len(tag.get_text(strip=True))


def link_density(tag: Tag) -> float:
    """Доля текста, находящегося внутри <a>, от всего текста тега."""
    total = text_len(tag)
    if total == 0:
        return 0.0
    link_text = sum(text_len(a) for a in tag.find_all("a"))
    return min(link_text / total, 1.0)


def class_id_string(tag: Tag) -> str:
    classes = " ".join(tag.get("class", []))
    return f"{classes} {tag.get('id', '')}".lower()


def matches_keywords(tag: Tag, keywords: list[str]) -> bool:
    s = class_id_string(tag)
    return any(kw in s for kw in keywords)


def _is_valid_css_ident(s: str) -> bool:
    """Проверяет, что строку можно безопасно использовать как CSS-класс/id
    без экранирования (буквы/цифры/дефис/подчёркивание, не начинается с цифры)."""
    return bool(re.match(r"^-?[A-Za-z_][A-Za-z0-9_-]*$", s))


def css_selector_for(tag: Tag) -> str:
    """Строит устойчивый css-селектор для тега: приоритет id -> tag+класс ->
    tag. Если значение id/класса содержит символы, недопустимые в CSS-
    идентификаторе без экранирования (например ':', ';', как в старой
    разметке SyntaxHighlighter: class="brush:py;"), используется атрибутный
    селектор вместо '#id'/'.class', чтобы не сгенерировать невалидный/
    некорректно интерпретируемый селектор."""
    if tag.get("id"):
        id_val = tag["id"]
        if _is_valid_css_ident(id_val):
            return f"#{id_val}"
        return f'{tag.name}[id="{id_val}"]'

    classes = tag.get("class")
    if classes:
        useful = [c for c in classes if not re.match(r"^(js-|is-|has-)", c)]
        cls = (useful or classes)[0]
        if _is_valid_css_ident(cls):
            return f"{tag.name}.{cls}"
        safe = cls.replace('"', '\\"')
        return f'{tag.name}[class~="{safe}"]'
    return tag.name


# --------------------------------------------------------------------------
# 1. Поиск тела статьи (article container) по текстовому скору
# --------------------------------------------------------------------------

def score_container(tag: Tag) -> float:
    """Скор в духе Readability: чем больше содержательного текста в
    прямых/вложенных <p> и чем ниже плотность ссылок — тем выше скор."""
    paragraphs = tag.find_all("p")
    good_paragraphs = [p for p in paragraphs if text_len(p) >= MIN_PARAGRAPH_LEN]
    if not good_paragraphs:
        return 0.0

    text_score = sum(text_len(p) for p in good_paragraphs)
    density = link_density(tag)
    penalty = 1.0 - min(density * 1.5, 0.9)  # высокая плотность ссылок душит скор
    # бонус за семантический тег <article>
    tag_bonus = 1.25 if tag.name == "article" else 1.0
    return text_score * penalty * tag_bonus


def find_article_container(soup: BeautifulSoup) -> Tag | None:
    candidates: list[tuple[float, Tag]] = []
    for tag in soup.find_all(CONTAINER_TAGS):
        if is_structural_chrome(tag):
            continue
        if any(is_structural_chrome(p) for p in tag.parents if isinstance(p, Tag)):
            continue
        s = score_container(tag)
        if s > 0:
            candidates.append((s, tag))

    if not candidates:
        return None

    candidates.sort(key=lambda x: x[0], reverse=True)
    best_score, best_tag = candidates[0]

    # отбрасываем "матрёшку": если родитель тоже в кандидатах с почти
    # таким же скором (текст не добавился), берём самый глубокий -
    # это и есть непосредственная обёртка статьи, а не <body>/<main> целиком.
    for s, t in candidates:
        if t in best_tag.find_all(True, recursive=True) or t is best_tag:
            if s >= best_score * 0.98:
                best_tag = t
                best_score = s

    if best_score < MIN_ARTICLE_SCORE:
        return None
    return best_tag


# --------------------------------------------------------------------------
# 2. Автор
# --------------------------------------------------------------------------

def find_author_selectors(soup: BeautifulSoup, article: Tag) -> list[str]:
    found: list[str] = []

    for meta in soup.find_all("meta", attrs={"name": "author"}):
        found.append('meta[name="author"]')
        break
    for meta in soup.find_all("meta", attrs={"property": "article:author"}):
        found.append('meta[property="article:author"]')
        break

    scope = article or soup
    for tag in scope.find_all(True):
        if tag.get("rel") and "author" in tag.get("rel"):
            found.append(css_selector_for(tag))
        elif tag.get("itemprop") == "author":
            found.append(css_selector_for(tag))
        elif matches_keywords(tag, AUTHOR_KEYWORDS) and text_len(tag) < 80:
            # ограничение по длине текста, чтобы не поймать блок-контейнер
            found.append(css_selector_for(tag))

    # дедуп с сохранением порядка
    seen = set()
    result = []
    for sel in found:
        if sel not in seen:
            seen.add(sel)
            result.append(sel)
    return result[:5]


# --------------------------------------------------------------------------
# 3. Контент (реальные текстовые узлы) и мусор (реклама/шеринг/related)
# --------------------------------------------------------------------------

def find_content_and_remove_selectors(article: Tag) -> tuple[list[str], list[str]]:
    content_selectors: set[str] = set()
    remove_selectors: set[str] = set()

    for tag in article.find_all(True):
        # явный мусор по ключевым словам класса/id
        if matches_keywords(tag, NOISE_KEYWORDS):
            remove_selectors.add(css_selector_for(tag))
            continue
        # рекламные теги
        if tag.name in ("iframe", "ins"):
            remove_selectors.add(css_selector_for(tag))
            continue
        # блок с высокой плотностью ссылок и малым текстом — типично для
        # "читайте также" / соцкнопок без явных классов. Тег без class/id
        # даёт слишком общий селектор (например голый "ul") — такой
        # пропускаем, чтобы не вырезать заодно легитимные списки/блоки.
        if tag.name in ("div", "section") and text_len(tag) > 0:
            density = link_density(tag)
            has_class_or_id = bool(tag.get("id") or tag.get("class"))
            if density > 0.7 and text_len(tag) < 400 and has_class_or_id:
                remove_selectors.add(css_selector_for(tag))
                continue

    # контентные узлы: параграфы/заголовки/цитаты с достаточным текстом,
    # не попавшие внутрь уже помеченных remove-блоков
    removed_tags = set()
    for sel_tag in article.find_all(True):
        if css_selector_for(sel_tag) in remove_selectors:
            removed_tags.update(id(t) for t in sel_tag.find_all(True))
            removed_tags.add(id(sel_tag))

    for tag in article.find_all(CONTENT_TAGS):
        if id(tag) in removed_tags:
            continue
        if tag.name == "p" and text_len(tag) < MIN_PARAGRAPH_LEN:
            continue
        # для контентных тегов используем голое имя тега, а не tag.class:
        # 1) они и так ищутся только внутри найденного ARTICLE_SELECTORS,
        #    специфичность класса тут не нужна;
        # 2) вариативные классы (например разные языки подсветки кода
        #    "brush:py;"/"brush:sql;" у SyntaxHighlighter) иначе плодят
        #    кучу дублирующих селекторов для одного и того же смысла.
        content_selectors.add(tag.name)

    return sorted(content_selectors), sorted(remove_selectors)


# --------------------------------------------------------------------------
# 4. Анализ одной страницы
# --------------------------------------------------------------------------

@dataclass
class PageAnalysis:
    article_selector: str | None
    author_selectors: list[str] = field(default_factory=list)
    content_selectors: list[str] = field(default_factory=list)
    remove_selectors: list[str] = field(default_factory=list)


def analyze_html(html: str) -> PageAnalysis:
    soup = BeautifulSoup(html, "lxml")
    clean_soup(soup)

    article = find_article_container(soup)
    if article is None:
        return PageAnalysis(article_selector=None)

    author_sel = find_author_selectors(soup, article)
    content_sel, remove_sel = find_content_and_remove_selectors(article)

    return PageAnalysis(
        article_selector=css_selector_for(article),
        author_selectors=author_sel,
        content_selectors=content_sel,
        remove_selectors=remove_sel,
    )


# --------------------------------------------------------------------------
# 5. Агрегация по нескольким страницам сайта (голосование)
# --------------------------------------------------------------------------

def aggregate(pages: list[PageAnalysis], min_vote_ratio: float = 0.34) -> dict:
    n = len(pages)
    min_votes = max(1, round(n * min_vote_ratio))

    article_votes = Counter(p.article_selector for p in pages if p.article_selector)
    article_selectors = [sel for sel, _ in article_votes.most_common()]

    def vote_list(getter) -> list[str]:
        c = Counter()
        for p in pages:
            for sel in getter(p):
                c[sel] += 1
        # remove/author-паттерны, повторяющиеся на нескольких страницах,
        # надёжнее — но при 1 странице просто берём всё, что нашли
        threshold = min_votes if n > 1 else 1
        return [sel for sel, cnt in c.most_common() if cnt >= threshold]

    return {
        "ARTICLE_SELECTORS": tuple(article_selectors) or ("article",),
        "AUTHOR_SELECTORS": tuple(vote_list(lambda p: p.author_selectors)),
        "CONTENT_SELECTORS": tuple(vote_list(lambda p: p.content_selectors)),
        "REMOVE_SELECTORS": tuple(vote_list(lambda p: p.remove_selectors)),
    }


# --------------------------------------------------------------------------
# 6. Запись selectors.py
# --------------------------------------------------------------------------

def _fmt_tuple(values: tuple[str, ...]) -> str:
    if not values:
        return "()"
    items = ",\n    ".join(repr(v) for v in values)
    return f"(\n    {items},\n)"


def write_selectors_module(site: str, result: dict, out_path: str) -> None:
    prefix = re.sub(r"[^0-9a-zA-Z_]", "_", site).upper()
    lines = [
        f'# Автоматически сгенерировано detector.py для сайта "{site}"',
        "",
        f"{prefix}_AUTHOR_SELECTORS = {_fmt_tuple(result['AUTHOR_SELECTORS'])}",
        "",
        f"{prefix}_ARTICLE_SELECTORS = {_fmt_tuple(result['ARTICLE_SELECTORS'])}",
        "",
        f"{prefix}_CONTENT_SELECTORS = {_fmt_tuple(result['CONTENT_SELECTORS'])}",
        "",
        f"{prefix}_REMOVE_SELECTORS = {_fmt_tuple(result['REMOVE_SELECTORS'])}",
        "",
    ]
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

BROWSER_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Cache-Control": "no-cache",
    "Referer": "https://www.google.com/",
}


def load_html(source: str, is_url: bool) -> str:
    if is_url:
        try:
            import requests
            resp = requests.get(source, headers=BROWSER_HEADERS, timeout=20, allow_redirects=True)
            resp.raise_for_status()
            resp.encoding = resp.encoding or resp.apparent_encoding
            return resp.text
        except ImportError:
            import urllib.request
            req = urllib.request.Request(source, headers=BROWSER_HEADERS)
            with urllib.request.urlopen(req, timeout=20) as resp:
                return resp.read().decode(resp.headers.get_content_charset() or "utf-8", errors="replace")
    with open(source, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("sources", nargs="+", help="Пути к html-файлам (или URL с флагом --url)")
    ap.add_argument("--site", required=True, help="Имя сайта — используется как префикс переменных")
    ap.add_argument("--out", default="selectors.py", help="Путь для выходного файла (по умолчанию selectors.py)")
    ap.add_argument("--url", action="store_true", help="Трактовать sources как URL, а не пути к файлам")
    args = ap.parse_args()

    analyses = []
    for src in args.sources:
        html = load_html(src, args.url)
        analysis = analyze_html(html)
        if analysis.article_selector is None:
            print(f"[!] {src}: не удалось найти тело статьи (пропускаю)", file=sys.stderr)
            continue
        analyses.append(analysis)
        print(f"[ok] {src}: article={analysis.article_selector!r}, "
              f"content={len(analysis.content_selectors)}, "
              f"remove={len(analysis.remove_selectors)}, "
              f"author={len(analysis.author_selectors)}")

    if not analyses:
        print("Не удалось проанализировать ни одну страницу.", file=sys.stderr)
        sys.exit(1)

    result = aggregate(analyses)
    write_selectors_module(args.site, result, args.out)
    print(f"\nГотово -> {args.out}")


if __name__ == "__main__":
    main()
