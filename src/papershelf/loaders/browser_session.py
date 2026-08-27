from __future__ import annotations

from playwright.sync_api import (
    Browser,
    BrowserContext,
    Page,
    Playwright,
    sync_playwright,
)

from papershelf.config.constants import HIDE_BROWSER_FLAG


class BrowserSession:
    """
    Управляет жизненным циклом Playwright и Chromium.

    Playwright и браузер запускаются один раз
    и используются для последовательных загрузок.
    """

    # ------------------------------------------------------------------

    def __init__(self) -> None:
        self._playwright: Playwright | None = None
        self._browser: Browser | None = None
        self._context: BrowserContext | None = None

    # ------------------------------------------------------------------

    def start(self) -> None:
        """
        Запустить браузерную сессию.

        Повторный запуск не выполняется,
        если сессия уже полностью создана.
        """

        print(
            "BrowserSession.start(): "
            f"session_id={id(self)}"
        )

        if self._context is not None:
            print(
                "BrowserSession.start(): "
                "context уже существует"
            )
            return

        print(
            "BrowserSession: sync_playwright().start()"
        )

        self._playwright = sync_playwright().start()

        print(
            "BrowserSession: chromium.launch()"
        )

        self._browser = self._playwright.chromium.launch(
            headless=HIDE_BROWSER_FLAG,
        )

        print(
            "BrowserSession: browser created "
            f"id={id(self._browser)}"
        )

        if self._browser is None:
            raise RuntimeError(
                "Playwright не создал Browser."
            )

        print(
            "BrowserSession: browser.new_context()"
        )

        self._context = self._browser.new_context(
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

        print(
            "BrowserSession: context created "
            f"id={id(self._context)}"
        )

    # ------------------------------------------------------------------

    def new_page(self) -> Page:
        """
        Создать новую вкладку.

        Returns
        -------
        Page
            Новая страница Playwright.
        """

        print(
            "BrowserSession.new_page(): "
            f"session_id={id(self)}"
        )

        self.start()

        if self._context is None:
            raise RuntimeError(
                "Browser context не создан."
            )

        print(
            "BrowserSession.new_page(): "
            "context.new_page()"
        )

        page = self._context.new_page()

        print(
            "BrowserSession.new_page(): "
            f"page_id={id(page)}"
        )

        return page

    # ------------------------------------------------------------------

    def close(self) -> None:
        """
        Полностью закрыть браузерную сессию.
        """

        print(
            "BrowserSession.close(): "
            f"session_id={id(self)}"
        )

        if self._context is not None:
            print(
                "BrowserSession: closing context"
            )

            self._context.close()
            self._context = None

        if self._browser is not None:
            print(
                "BrowserSession: closing browser"
            )

            self._browser.close()
            self._browser = None

        if self._playwright is not None:
            print(
                "BrowserSession: stopping playwright"
            )

            self._playwright.stop()
            self._playwright = None

        print(
            "BrowserSession.close(): DONE"
        )