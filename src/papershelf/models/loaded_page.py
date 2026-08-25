from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class LoadedPage:
    """
    Загруженная веб-страница.
    """

    url: str

    html: str