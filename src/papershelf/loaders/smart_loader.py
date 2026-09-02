from __future__ import annotations

import requests

from papershelf.core.exceptions import PageNotFoundError
from papershelf.loaders.browser_loader import BrowserLoader
from papershelf.loaders.dynamic_site_detector import DynamicSiteDetector
from papershelf.loaders.http_loader import HttpLoader
from papershelf.loaders.page_loader import PageLoader
from papershelf.models.loaded_page import LoadedPage
from papershelf.services.http_fallback_policy import HttpFallbackPolicy


class SmartLoader(PageLoader):
    """
    Автоматически выбирает способ
    загрузки страницы.
    """

    # ------------------------------------------------------------------
    
    def __init__(
            self,
    ) -> None:
        """
        Инициализировать загрузчики и сервисы.
        """
        
        self._http = HttpLoader()
        
        self._browser = BrowserLoader()
        
        self._detector = DynamicSiteDetector()
        
        self._fallback_policy = HttpFallbackPolicy()

    # ------------------------------------------------------------------
    
    def load(
            self,
            url: str,
    ) -> LoadedPage:
        """
        Загрузить страницу подходящим способом.

        Сначала выполняется загрузка через HttpLoader.
        Если HTTP-загрузка завершилась ошибкой, решение
        о переходе к BrowserLoader принимает HttpFallbackPolicy.

        Ошибка 404 преобразуется в доменное исключение
        PaperShelfError и не передается BrowserLoader.

        После успешной HTTP-загрузки определяется,
        является ли страница динамической. Для динамических
        страниц используется BrowserLoader.
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
        # HTTP-ошибка.
        #
        except requests.HTTPError as exc:
            
            status_code = None
            
            if exc.response is not None:
                status_code = exc.response.status_code
            
            print(
                "SmartLoader: HTTP error "
                f"status={status_code}"
            )
            
            #
            # 404 — страница действительно отсутствует.
            #
            if status_code == 404:
                raise PageNotFoundError(
                    url,
                ) from exc
            
            #
            # Остальные HTTP-ошибки передаем
            # в HttpFallbackPolicy.
            #
            if not self._fallback_policy.should_use_browser(
                    status_code,
            ):
                print(
                    "SmartLoader: "
                    "BrowserLoader не используется"
                )
                
                raise
            
            print(
                "SmartLoader: "
                "switching to BrowserLoader"
            )
            
            return self._browser.load(
                url,
            )
        
        #
        # Остальные ошибки requests.
        #
        except requests.RequestException as exc:
            
            print(
                f"SmartLoader: HTTP failed ({exc})"
            )
            
            print(
                "SmartLoader: "
                "switching to BrowserLoader"
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