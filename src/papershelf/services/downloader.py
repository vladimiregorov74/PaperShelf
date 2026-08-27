from __future__ import annotations

from requests import Session
from requests.exceptions import RequestException


DEFAULT_TIMEOUT = 100


class DownloaderService:
    """
    Универсальный сервис загрузки ресурсов.
    """

    # ------------------------------------------------------------------

    def __init__(self) -> None:

        self._session = Session()

        self._session.headers.update(
            {
                "User-Agent": (
                    "Mozilla/5.0 "
                    "(X11; Linux x86_64) "
                    "AppleWebKit/537.36 "
                    "(KHTML, like Gecko) "
                    "Chrome/138.0.0.0 "
                    "Safari/537.36"
                )
            }
        )

    # ------------------------------------------------------------------

    def download(self, url: str) -> str:
        """
        Скачать HTML страницы.
        """
        
        import traceback
        
        print()
        print("=" * 80)
        print("DownloaderService.download()")
        traceback.print_stack(limit=8)
        print("=" * 80)
        
        response = self._get(url)

        return response.text

    # ------------------------------------------------------------------

    def download_binary(self, url: str) -> bytes:
        """
        Скачать бинарный ресурс.

        Используется для:

            - изображений
            - PDF
            - CSS
            - SVG
            - шрифтов
            - вложений
        """

        response = self._get(url)

        return response.content

    # ------------------------------------------------------------------

    def _get(self, url: str):
        """
        Выполнить GET-запрос.
        """

        try:

            response = self._session.get(
                url,
                timeout=DEFAULT_TIMEOUT,
            )

            response.raise_for_status()

            return response

        except RequestException as exc:

            raise RuntimeError(
                f"Не удалось скачать ресурс:\n{url}"
            ) from exc