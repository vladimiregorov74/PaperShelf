from __future__ import annotations

from papershelf.loaders.browser_loader import BrowserLoader
from papershelf.loaders.dynamic_site_detector import DynamicSiteDetector
from papershelf.loaders.http_loader import HttpLoader
from papershelf.loaders.page_loader import PageLoader
from papershelf.models.loaded_page import LoadedPage


class SmartLoader(PageLoader):
    """
    Автоматически выбирает способ
    загрузки страницы.
    """

    # ------------------------------------------------------------------

    def __init__(self, ) -> None:
        
        self._http = HttpLoader()
        
        self._browser = BrowserLoader()
        
        self._detector = DynamicSiteDetector()

    # ------------------------------------------------------------------
    
    def load(
            self,
            url: str,
    ) -> LoadedPage:
        
        page = self._http.load(
            url,
        )
        
        if self._detector.is_dynamic(
                page.html,
        ):
            return self._browser.load(
                url,
            )
        
        return page