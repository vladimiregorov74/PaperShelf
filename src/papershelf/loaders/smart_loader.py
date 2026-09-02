from __future__ import annotations

import requests

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

    def __init__(self) -> None:
        self._http = HttpLoader()

        self._browser = BrowserLoader()

        self._detector = DynamicSiteDetector()

    # ------------------------------------------------------------------
    
    def load(
            self,
            url: str,
    ) -> LoadedPage:
        """
        Загрузить страницу подходящим способом.
        """
        
        print(
            f"SmartLoader.load(): START id={id(self)} url={url}"
        )
        
        #
        # Сначала пробуем обычный HTTP.
        #
        try:
            
            print(
                "SmartLoader: HTTP load START"
            )
            
            page = self._http.load(
                url,
            )
            
            print(
                "SmartLoader: HTTP load END "
                f"html={len(page.html)}"
            )
        
        #
        # Если requests не справился —
        # пробуем полноценный браузер.
        #
        except requests.HTTPError as exc:
            
            if exc.response is not None:
                if exc.response.status_code == 404:
                    raise
            
            return self._browser.load(url)
        except requests.RequestException as exc:
            
            print(
                f"SmartLoader: HTTP failed ({exc})"
            )
            
            print(
                "SmartLoader: switching to BrowserLoader"
            )
            
            return self._browser.load(
                url,
            )
        
        print(
            "SmartLoader: проверяем dynamic"
        )
        
        dynamic = self._detector.is_dynamic(
            page.html,
        )
        
        print(
            f"SmartLoader: dynamic={dynamic}"
        )
        
        if dynamic:
            print(
                "SmartLoader: BrowserLoader"
            )
            
            page = self._browser.load(
                url,
            )
        
        print(
            f"SmartLoader.load(): END page id={id(page)}"
        )
        
        return page

    # ------------------------------------------------------------------

    def close(self) -> None:
        """
        Освободить ресурсы загрузчиков.
        """

        self._browser.close()