from __future__ import annotations

import requests

from papershelf.loaders.page_loader import PageLoader
from papershelf.models.loaded_page import LoadedPage


class HttpLoader(PageLoader):
    """
    Загрузка страницы через requests.
    """

    # ------------------------------------------------------------------

    def load(
        self,
        url: str,
    ) -> LoadedPage:

        response = requests.get(
            url,
            timeout=30,
            headers={
                "User-Agent":
                    (
                        "Mozilla/5.0 "
                        "(X11; Linux x86_64) "
                        "AppleWebKit/537.36 "
                        "(KHTML, like Gecko) "
                        "Chrome/138.0 Safari/537.36"
                    )
            },
        )
        print("httploader.load response = ", response.text)
        response.raise_for_status()

        return LoadedPage(
                            url=url,
                            html=response.text,
                        )