from __future__ import annotations

from dataclasses import dataclass, field
from bs4 import Tag


# ------------------------------------------------------------------
# Page
# ------------------------------------------------------------------


@dataclass(slots=True)
class PageInfo:
    """
    Общая информация о странице.
    """

    url: str

    title: str

    encoding: str = ""


# ------------------------------------------------------------------
# Heading
# ------------------------------------------------------------------


@dataclass(slots=True)
class HeadingInfo:
    """
    Информация о заголовке.
    """

    level: int

    text: str

    selector: str


# ------------------------------------------------------------------
# Image
# ------------------------------------------------------------------


@dataclass(slots=True)
class ImageInfo:
    """
    Информация об изображении.
    """

    src: str

    alt: str = ""

    extension: str = ""


# ------------------------------------------------------------------
# Code block
# ------------------------------------------------------------------


@dataclass(slots=True)
class CodeBlockInfo:
    """
    Информация о блоке исходного кода.
    """

    tag: str

    language: str

    classes: list[str] = field(default_factory=list)

    lines: int = 0

    text: str = ""


# ------------------------------------------------------------------
# Table
# ------------------------------------------------------------------


@dataclass(slots=True)
class TableInfo:
    """
    Информация о HTML-таблице.
    """

    rows: int

    columns: int
    
    css_classes: list[str] = field(default_factory=list)

# ------------------------------------------------------------------
# Link
# ------------------------------------------------------------------


@dataclass(slots=True)
class LinkInfo:
    """
    Информация о гиперссылке.
    """

    href: str

    text: str

    external: bool


# ------------------------------------------------------------------
# Container
# ------------------------------------------------------------------


@dataclass(slots=True)
class ContainerInfo:
    """
    Информация о контейнере страницы.
    """

    tag: str

    css_id: str

    css_classes: list[str]

    text_length: int

    paragraphs: int

    headings: int

    images: int

    code_blocks: int

    tables: int

    links: int

    score: float = 0.0


# ------------------------------------------------------------------
# Statistics
# ------------------------------------------------------------------


@dataclass(slots=True)
class StatisticsInfo:
    """
    Общая статистика страницы.
    """

    headings: int

    images: int

    code_blocks: int

    tables: int

    links: int

    containers: int


# ------------------------------------------------------------------
# Inspection report
# ------------------------------------------------------------------


@dataclass(slots=True)
class InspectionReport:
    """
    Полный результат анализа страницы.
    """

    page: PageInfo

    statistics: StatisticsInfo

    headings: list[HeadingInfo]

    images: list[ImageInfo]

    code_blocks: list[CodeBlockInfo]

    tables: list[TableInfo]

    links: list[LinkInfo]

    containers: list[ContainerInfo]
    
    article_candidate: ArticleCandidate | None = None
    
    cleaning_report: CleaningReport | None = None
    
    author_selectors: list[str] = field(
        default_factory=list,
    )

# ------------------------------------------------------------------
# Container analysis
# ------------------------------------------------------------------

@dataclass(slots=True)
class ContainerAnalysis:
    """
    Подробный анализ выбранного контейнера.
    """

    selector: str

    children: list[ChildInfo]

    headings: list[HeadingInfo]

    images: list[ImageInfo]

    code_blocks: list[CodeBlockInfo]

    tables: list[TableInfo]

    links: list[LinkInfo]

    classes: dict[str, int]


# ------------------------------------------------------------------
# Child Info
# ------------------------------------------------------------------

@dataclass(slots=True)
class ChildInfo:
    """
    Информация о дочернем контейнере.
    """

    tag: str

    selector: str

    css_id: str

    css_classes: list[str]

    text_length: int

    paragraphs: int

    headings: int

    images: int

    code_blocks: int

    tables: int

    links: int
    
    link_text_length: int
    
    plain_text_length: int

    # Прямая ссылка на сам HTML-элемент. Критично: без неё переход
    # к дочернему контейнеру в ArticleDetector делает повторный поиск
    # по CSS-селектору (parent.select_one(selector)), а если у элемента
    # нет id/class, селектор вырождается в голое имя тега ("div") —
    # select_one находит ПЕРВЫЙ подходящий элемент в поддереве, а не
    # тот самый, что был оценён. На сайтах с безымянными div-обёртками
    # (React/Vue-приложения вроде Habr) это уводит детектор в случайную
    # часть страницы. Храня сам Tag, переход становится однозначным.
    element: Tag

    score: float = 0.0
    
# ------------------------------------------------------------------
# Article detection
# ------------------------------------------------------------------

@dataclass(slots=True)
class ArticleCandidate:
    """
    Найденный контейнер статьи.
    """

    selector: str

    score: float

    depth: int

    path: list[str]

    analysis: ContainerAnalysis

    element: Tag
    
# ------------------------------------------------------------------
# Cleaning Decision
# ------------------------------------------------------------------

@dataclass(slots=True)
class CleaningDecision:
    """
    Решение по конкретному элементу.
    """

    selector: str

    action: str

    score: float

    reason: str

# ------------------------------------------------------------------
# Cleaning Report
# ------------------------------------------------------------------

@dataclass(slots=True)
class CleaningReport:
    """
    Результат анализа контейнера.
    """

    keep: list[CleaningDecision]

    remove: list[CleaningDecision]

# ------------------------------------------------------------------
# Noise Info
# ------------------------------------------------------------------

@dataclass(slots=True)
class NoiseInfo:
    """
    Информация о потенциально служебном HTML-элементе.
    """

    selector: str

    score: float

    reason: str

    remove: bool

















