from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class SupportedSite:
    """
    Описание поддерживаемого сайта.
    """

    identifier: str
    domain: str
    source: str
    title_suffix: str