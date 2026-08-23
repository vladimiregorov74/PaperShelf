from __future__ import annotations

from papershelf.loaders.http_loader import HttpLoader
from papershelf.loaders.page_loader import PageLoader
from papershelf.loaders.dynamic_site_detector import (
    DynamicSiteDetector,
)


class SmartLoader(PageLoader):
    """
    Автоматически выбирает способ
    загрузки страницы.
    """

    # ------------------------------------------------------------------

    def __init__(
        self,
    ) -> None:
        self._http = HttpLoader()

        self._detector = DynamicSiteDetector()

    # ------------------------------------------------------------------

    def load(
            self,
            url: str,
    ) -> str:
        html = self._http.load(
            url,
        )

        if self._detector.is_dynamic(
                html,
        ):
            #
            # Пока BrowserLoader
            # еще не реализован.
            #
            return self._browser.load(url)

        return html