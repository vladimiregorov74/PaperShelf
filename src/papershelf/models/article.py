from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(slots=True)
class Article:
    """
    Модель статьи.
    """

    url: str

    title: str = ""

    author: str = ""

    source: str = ""

    html: str = ""

    text: str = ""

    created_at: datetime = field(default_factory=datetime.now)  # время создаётся при создании каждого объекта