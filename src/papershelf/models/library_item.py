from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class LibraryItem:
    """
    Элемент библиотеки статей.
    """

    title: str

    author: str

    source: str

    directory: Path

    created_at: str
    
    url: str