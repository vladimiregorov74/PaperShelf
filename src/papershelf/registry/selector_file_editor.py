from __future__ import annotations

from pathlib import Path


class SelectorFileEditor:
    """
    Редактор selectors.py.
    """

    # ------------------------------------------------------------------

    def __init__(
        self,
        path: Path,
    ) -> None:

        self._path = path
    
    def remove(
            self,
            identifier: str,
    ) -> None:
        """
        Удалить селекторы сайта.
        """
        
        # raise NotImplementedError