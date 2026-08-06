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

