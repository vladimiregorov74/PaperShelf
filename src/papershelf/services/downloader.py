from __future__ import annotations

from requests import Session
from requests.exceptions import RequestException


DEFAULT_TIMEOUT = 20


class DownloaderService:
    """
    Сервис загрузки HTML-страниц.
    """

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

        Parameters
        ----------
        url:
            Адрес страницы.

        Returns
        -------
        str
            HTML страницы.

        Raises
        ------
        RuntimeError
            Если страницу получить не удалось.
        """

        try:

            response = self._session.get(
                url,
                timeout=DEFAULT_TIMEOUT,
            )

            response.raise_for_status()

            return response.text

        except RequestException as exc:
            raise RuntimeError(
                f"Не удалось скачать страницу:\n{url}"
            ) from exc