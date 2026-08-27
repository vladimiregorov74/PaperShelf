from __future__ import annotations

from playwright.sync_api import (
    Page,
    TimeoutError as PlaywrightTimeoutError,
)

from papershelf.loaders.browser_session import BrowserSession
from papershelf.loaders.page_loader import PageLoader
from papershelf.models.loaded_page import LoadedPage


class BrowserLoader(PageLoader):
    """
    Загрузка страниц через Chromium.

    Ожидание готовности страницы не зависит от конкретного сайта.
    Используются несколько общих признаков:

    - DOM загружен;
    - сеть по возможности затихла;
    - DOM некоторое время не изменяется;
    - страница прокручена для активации ленивой загрузки;
    - после прокрутки снова ожидается стабильность DOM.
    """

    _NETWORK_IDLE_TIMEOUT_MS = 10_000

    _DOM_QUIET_MS = 800

    _DOM_QUIET_TIMEOUT_MS = 15_000

    # ------------------------------------------------------------------

    def __init__(
        self,
        session: BrowserSession | None = None,
    ) -> None:
        self._session = session or BrowserSession()

        print(
            "BrowserLoader.__init__(): "
            f"loader_id={id(self)} "
            f"session_id={id(self._session)}"
        )

    # ------------------------------------------------------------------

    def load(
        self,
        url: str,
    ) -> LoadedPage:
        """
        Загрузить HTML после выполнения JavaScript.
        """

        print(
            "BrowserLoader.load(): START "
            f"loader_id={id(self)} "
            f"session_id={id(self._session)}"
        )

        page = self._session.new_page()

        try:
            print(
                "BrowserLoader: page.goto()"
            )

            page.goto(
                url,
                wait_until="domcontentloaded",
                timeout=30_000,
            )

            print(
                f"BrowserLoader: page.url={page.url}"
            )

            print(
                f"BrowserLoader: title={page.title()!r}"
            )

            self._install_mutation_observer(
                page,
            )

            self._wait_for_network_idle(
                page,
            )

            self._wait_for_dom_quiet(
                page,
            )

            self._scroll_through(
                page,
            )

            self._wait_for_dom_quiet(
                page,
            )

            html = page.content()

            print(
                "BrowserLoader: HTML получен "
                f"length={len(html)}"
            )

            return LoadedPage(
                url=page.url,
                html=html,
            )

        finally:
            print(
                "BrowserLoader: закрываем Page"
            )

            page.close()

            print(
                "BrowserLoader.load(): END"
            )

    # ------------------------------------------------------------------

    @staticmethod
    def _install_mutation_observer(
        page: Page,
    ) -> None:
        """
        Установить MutationObserver для отслеживания
        изменений DOM.
        """

        print(
            "BrowserLoader: устанавливаем MutationObserver"
        )

        page.evaluate(
            """
            () => {
                window.__lastMutationAt = Date.now();

                if (!window.__mutationObserverInstalled) {
                    window.__mutationObserverInstalled = true;

                    new MutationObserver(() => {
                        window.__lastMutationAt = Date.now();
                    }).observe(
                        document.documentElement,
                        {
                            childList: true,
                            subtree: true,
                            characterData: true,
                            attributes: true,
                        }
                    );
                }
            }
            """,
        )

    # ------------------------------------------------------------------

    def _wait_for_network_idle(
        self,
        page: Page,
    ) -> None:
        """
        Дождаться затихания сетевой активности.

        Ожидание не является обязательным: некоторые сайты
        поддерживают постоянные фоновые соединения.
        """

        print(
            "BrowserLoader: "
            "ожидание networkidle..."
        )

        try:
            page.wait_for_load_state(
                "networkidle",
                timeout=self._NETWORK_IDLE_TIMEOUT_MS,
            )

            print(
                "BrowserLoader: "
                "networkidle достигнут"
            )

        except PlaywrightTimeoutError:
            print(
                "BrowserLoader: "
                "networkidle не достигнут — продолжаем"
            )

    # ------------------------------------------------------------------

    def _wait_for_dom_quiet(
        self,
        page: Page,
    ) -> None:
        """
        Дождаться отсутствия изменений DOM.
        """

        print(
            "BrowserLoader: "
            "ожидание стабильности DOM..."
        )

        try:
            page.wait_for_function(
                """
                quietMs => {
                    return (
                        Date.now()
                        - (window.__lastMutationAt || 0)
                    ) > quietMs;
                }
                """,
                arg=self._DOM_QUIET_MS,
                timeout=self._DOM_QUIET_TIMEOUT_MS,
            )

            print(
                "BrowserLoader: "
                "DOM стабилен"
            )

        except PlaywrightTimeoutError:
            print(
                "BrowserLoader: "
                "DOM не стабилизировался — продолжаем"
            )

    # ------------------------------------------------------------------

    @staticmethod
    def _scroll_through(
        page: Page,
    ) -> None:
        """
        Прокрутить страницу сверху вниз и обратно.

        Используется для активации ленивой загрузки
        и виртуализированного контента.
        """

        print(
            "BrowserLoader: "
            "прокручиваем страницу"
        )

        page.evaluate(
            """
            async () => {
                const step = window.innerHeight;
                let last = -1;

                while (
                    document.scrollingElement.scrollTop !== last
                ) {
                    last =
                        document.scrollingElement.scrollTop;

                    window.scrollBy(
                        0,
                        step,
                    );

                    await new Promise(
                        resolve => setTimeout(resolve, 200)
                    );
                }

                window.scrollTo(0, 0);
            }
            """,
        )

        print(
            "BrowserLoader: "
            "прокрутка завершена"
        )

    # ------------------------------------------------------------------

    def close(self) -> None:
        """
        Закрыть браузерную сессию.
        """

        print(
            "BrowserLoader.close(): "
            f"loader_id={id(self)}"
        )

        self._session.close()