from __future__ import annotations

import traceback

from playwright.sync_api import (
    sync_playwright,
    TimeoutError as PlaywrightTimeoutError,
)

from papershelf.loaders.page_loader import PageLoader
from papershelf.models.loaded_page import LoadedPage


class BrowserLoader(PageLoader):
    """
    Загрузка страницы через Chromium.
    """

    # ------------------------------------------------------------------

    # def load(
    #     self,
    #     url: str,
    # ) -> str:
    #     """
    #     Загрузить HTML после выполнения JavaScript.
    #     """
    #
    #     with sync_playwright() as playwright:
    #         browser = playwright.chromium.launch(
    #             headless=False,
    #         )
    #         context = browser.new_context(
    #             user_agent=(
    #                 "Mozilla/5.0 "
    #                 "(X11; Linux x86_64) "
    #                 "AppleWebKit/537.36 "
    #                 "(KHTML, like Gecko) "
    #                 "Chrome/138.0 Safari/537.36"
    #             ),
    #             locale="ru-RU",
    #             viewport={
    #                 "width": 1600,
    #                 "height": 900,
    #             },
    #         )
    #         # page = browser.new_page()
    #         page = context.new_page()
    #         page.goto(
    #             url,
    #             wait_until="domcontentloaded",
    #             timeout=30000,
    #         )
    #         print(f"{page.url=}")
    #         print(f"{page.title()=}")
    #         # page.wait_for_timeout(
    #         #     10000,
    #         # )
    #         page.wait_for_selector(
    #             ".notion-page-content",
    #             timeout=30000,
    #         )
    #
    #         html = page.content()
    #         print(f"{html[:1000]=}")
    #
    #         browser.close()
    #
    #         return html
    
    def load(
            self,
            url: str,
    ) -> LoadedPage:
        """
        Загрузить HTML после выполнения JavaScript.
        """
        
        print()
        print("=" * 80)
        print("BrowserLoader.load()")
        traceback.print_stack(limit=8)
        print("=" * 80)
        
        with sync_playwright() as playwright:
            
            browser = playwright.chromium.launch(
                headless=False,
            )
            
            try:
                context = browser.new_context(
                    user_agent=(
                        "Mozilla/5.0 "
                        "(X11; Linux x86_64) "
                        "AppleWebKit/537.36 "
                        "(KHTML, like Gecko) "
                        "Chrome/138.0 Safari/537.36"
                    ),
                    locale="ru-RU",
                    viewport={
                        "width": 1600,
                        "height": 900,
                    },
                )
                
                page = context.new_page()
                
                print("BrowserLoader: page.goto()")
                
                page.goto(
                    url,
                    wait_until="domcontentloaded",
                    timeout=30000,
                )
                
                print(f"{page.url=}")
                print(f"{page.title()=}")
                
                try:
                    page.wait_for_selector(
                        ".notion-page-content",
                        timeout=30000,
                    )
                
                except PlaywrightTimeoutError as exc:
                    
                    print(
                        "BrowserLoader: не дождались "
                        f".notion-page-content ({exc})"
                    )
                
                html = page.content()
                
                print(
                    f"BrowserLoader: получено {len(html)} символов, "
                    f"'notion-page-content' в html: "
                    f"{'notion-page-content' in html}"
                )
                
                return LoadedPage(url=url, html=html,)
            
            finally:
                print("BrowserLoader.close()")
                browser.close()