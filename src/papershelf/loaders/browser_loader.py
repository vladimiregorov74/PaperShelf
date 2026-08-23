from __future__ import annotations

from papershelf.loaders.page_loader import PageLoader


class BrowserLoader(PageLoader):
    """
    Загрузка страницы в браузере.
    """

    def __init__(self):
        self._playwright = None
        self._browser = BrowserLoader()
    # ------------------------------------------------------------------

    def load(
        self,
        url: str,
    ) -> str:

        raise NotImplementedError