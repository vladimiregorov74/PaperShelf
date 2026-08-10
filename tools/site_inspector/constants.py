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

ARTICLE_MIN_CHILD_SCORE = 100.0

ARTICLE_MIN_TEXT_LENGTH = 300

ARTICLE_MAX_LINK_DENSITY = 0.35

ARTICLE_MIN_PARAGRAPHS = 3

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

