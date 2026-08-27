from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class LibraryStatistics:
    """
    Статистика библиотеки.
    """

    article_count: int

    library_size: int