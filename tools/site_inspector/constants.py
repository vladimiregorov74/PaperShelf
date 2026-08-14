LANGUAGE_ALIASES = {
    # Python
    "py": "python",
    "python": "python",

    # C / C++
    "c": "c",
    "cpp": "cpp",
    "c++": "cpp",

    # C#
    "cs": "csharp",
    "csharp": "csharp",

    # Java
    "java": "java",

    # JavaScript
    "js": "javascript",
    "javascript": "javascript",

    # TypeScript
    "ts": "typescript",
    "typescript": "typescript",

    # SQL
    "sql": "sql",

    # HTML / CSS
    "html": "html",
    "css": "css",

    # JSON / XML / YAML
    "json": "json",
    "xml": "xml",
    "yaml": "yaml",
    "yml": "yaml",

    # Shell
    "sh": "shell",
    "shell": "shell",
    "bash": "bash",

    # PowerShell
    "ps1": "powershell",
    "powershell": "powershell",
}

LANGUAGE_PREFIXES = (
    "language-",
    "lang-",
    "brush:",
    "brush-",
)
MIN_CONTAINER_TEXT = 100
TEXT_WEIGHT = 0.01
PARAGRAPH_WEIGHT = 10
HEADING_WEIGHT = 15
IMAGE_WEIGHT = 3
CODE_WEIGHT = 8
TABLE_WEIGHT = 5
LINK_WEIGHT = -0.2

REPORT_WIDTH = 70

POSITIVE_CLASSES = {
    "article": 40,
    "content": 30,
    "main": 20,
    "post": 20,
}

NEGATIVE_CLASSES = {
    "menu": -100,
    "sidebar": -80,
    "footer": -80,
    "header": -80,
    "nav": -80,
    "advert": -100,
}
# ------------------------------------------------------------------
# Article detector
# ------------------------------------------------------------------

ARTICLE_MIN_CHILD_SCORE = 50.0

ARTICLE_MIN_TEXT_LENGTH = 300

ARTICLE_MAX_LINK_DENSITY = 0.35

ARTICLE_MIN_PARAGRAPHS = 3

# Порог для относительной проверки при спуске к дочернему контейнеру:
# ребёнок должен содержать не меньше этой доли текста ТЕКУЩЕГО
# контейнера, иначе это не "продолжение того же контейнера через
# обёртку", а провал внутрь отдельного фрагмента статьи (например,
# один <ul> с парой пунктов внутри огромной статьи может набрать
# ARTICLE_MIN_CHILD_SCORE баллов за счёт кода в <li>, но составляет
# лишь доли процента текста всей статьи). Без этой проверки
# ARTICLE_MIN_CHILD_SCORE как абсолютное число откалибровано под ОДИН
# масштаб страниц и ломается на сайтах с сильно другим объёмом
# контента (маленькие страницы metanit vs огромные статьи habr).
ARTICLE_CHILD_DOMINANCE_RATIO = 0.6

# ------------------------------------------------------------------
# Cleaner
# ------------------------------------------------------------------

KEEP_SCORE_THRESHOLD = 0.0


# ------------------------------------------------------------------
# Text scoring
# ------------------------------------------------------------------

TEXT_LENGTH_FACTOR = 0.02

PARAGRAPH_SCORE = 2.0

HEADING_SCORE = 4.0


# ------------------------------------------------------------------
# Code scoring
# ------------------------------------------------------------------

CODE_BLOCK_SCORE = 8.0

CODE_LINE_FACTOR = 0.05


# ------------------------------------------------------------------
# Tables
# ------------------------------------------------------------------

TABLE_SCORE = 2.0


# ------------------------------------------------------------------
# Images
# ------------------------------------------------------------------

IMAGE_SCORE = 1.0


# ------------------------------------------------------------------
# Links
# ------------------------------------------------------------------

LINK_PENALTY = 0.5

LINK_DENSITY_THRESHOLD = 0.10

LINK_DENSITY_PENALTY = 15.0

# ------------------------------------------------------------------
# Selector penalties
# ------------------------------------------------------------------

NAV_PENALTY = 40.0

FOOTER_PENALTY = 35.0

SIDEBAR_PENALTY = 30.0

SOCIAL_PENALTY = 35.0

COMMENT_PENALTY = 25.0

ADVERTISEMENT_PENALTY = 40.0

# ------------------------------------------------------------------
# Selector penalties
# ------------------------------------------------------------------

SELECTOR_PENALTIES: dict[str, float] = {
    "nav": 40.0,
    "menu": 35.0,

    "footer": 35.0,
    "header": 20.0,

    "sidebar": 30.0,
    "aside": 30.0,

    "soc": 35.0,
    "social": 35.0,
    "share": 35.0,

    "comment": 25.0,
    "comments": 25.0,

    "banner": 40.0,
    "ads": 40.0,
    "advert": 40.0,

    "promo": 25.0,

    "pagination": 30.0,
}

# ------------------------------------------------------------------
# Selector bonuses
# ------------------------------------------------------------------

SELECTOR_BONUSES: dict[str, float] = {
    "article": 30.0,
    "content": 25.0,
    "post": 20.0,
    "body": 20.0,

    "main": 15.0,

    "text": 15.0,

    "code": 10.0,

    "syntax": 10.0,
}
# ------------------------------------------------------------------
# Structure scoring
# ------------------------------------------------------------------

STRUCTURE_TEXT_BONUS = 3.0

STRUCTURE_HEADING_BONUS = 5.0

STRUCTURE_CODE_BONUS = 8.0

STRUCTURE_IMAGE_BONUS = 3.0

STRUCTURE_TABLE_BONUS = 4.0

# ------------------------------------------------------------------
# Noise analysis
# ------------------------------------------------------------------

NOISE_REMOVE_THRESHOLD = 10.0

NOISE_NAV_SCORE = 40.0

NOISE_SOCIAL_SCORE = 30.0

NOISE_DATE_SCORE = 20.0

# ------------------------------------------------------------------
# Расширенный словарь ключевых слов для классификации шума.
# Сравнение — по целым словам/токенам класса (после разбиения по
# "-", "_" и camelCase), а не по подстроке всего селектора — поэтому
# "tm-article-meta" ловится по токену "meta", а не по случайному
# совпадению внутри более длинного слова.
# ------------------------------------------------------------------

NOISE_CLASS_KEYWORDS = [
    "nav", "navigation", "menu", "breadcrumb", "breadcrumbs",
    "social", "soc", "share", "sharing", "socblock",
    "related", "recommend", "recommended", "also",
    "comment", "comments", "disqus",
    "widget", "popup", "modal", "cookie", "paywall",
    "teaser", "promo", "sponsor", "subscribe", "subscription", "newsletter",
    "banner", "advert", "adverts", "ads", "adsbygoogle",
    "pagination", "pager", "toolbar",
    "meta", "date", "datetime", "publish", "published",
    "hub", "hubs", "tag", "tags", "taglist", "rating",
    "sidebar", "aside", "footer", "header",
]

# ------------------------------------------------------------------
# Известные маркеры рекламных сетей — сверяются как ПРЕФИКС значения
# id/class (не токен), рекурсивно по всему контейнеру статьи, а не
# только среди прямых детей. Это отдельный механизм от обычного
# скоринга/NOISE_CLASS_KEYWORDS: рекламный слот часто сам без класса
# лежит в безымянной div-обёртке ("<div style=...><div id='yandex_rtb_
# ...'></div></div>") — обёртка получает score=0 и попадает в decision
# с reason="zero score", а такие decision намеренно исключаются из
# генерации REMOVE_SELECTORS (иначе туда попал бы голый "div" без
# класса/id, что вырезало бы вообще всё). Прямой поиск по маркеру
# рекламной сети даёт точный, безопасный для генерации селектор вида
# 'div[id^="yandex_rtb"]', не зависящий от места элемента в дереве.
# ------------------------------------------------------------------

AD_NETWORK_ID_PREFIXES = [
    "yandex_rtb",
    "yandex-rtb",
    "adfox",
    "google_ads",
    "div-gpt-ad",
]

AD_NETWORK_CLASS_MARKERS = [
    "adfox",
    "adsbygoogle",
    "smi2",
    "recommby",
    "mgid",
]

