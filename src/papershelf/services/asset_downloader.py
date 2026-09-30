from __future__ import annotations

import base64
from pathlib import Path
from urllib.parse import unquote
from urllib.parse import urljoin
from urllib.parse import urlparse

from bs4 import BeautifulSoup

from papershelf.models import Article
from papershelf.services.downloader import DownloaderService


class AssetDownloader:
    """
    Скачивает ресурсы статьи.

    Поддерживаются:

    - img[src]
    - source[srcset]
    - внешние SVG
    - SVG в формате Data URI

    После загрузки заменяет ссылки
    в article.html на локальные.
    """

    # ------------------------------------------------------------------

    def __init__(
        self,
        downloader: DownloaderService,
    ) -> None:

        self._downloader = downloader

    # ------------------------------------------------------------------

    def process(
        self,
        article: Article,
        directory: Path,
        logger=None,
    ) -> None:
        """
        Скачать ресурсы статьи.

        Parameters
        ----------
        article:
            Статья с исходным HTML.

        directory:
            Каталог, в котором сохраняется статья.

        logger:
            Необязательная функция для вывода сообщений.
        """

        soup = BeautifulSoup(
            article.html,
            "lxml",
        )

        assets_dir = directory / "assets"

        assets_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        counter = 1

        #
        # img
        #
        for image in soup.find_all("img"):

            src = image.get("src")

            if not src:
                continue

            local = self._download_asset(
                src,
                article.url,
                assets_dir,
                counter,
                logger,
            )

            if not local:
                continue

            image["src"] = local

            #
            # После сохранения изображения локально
            # браузер сам определит его реальные размеры.
            #
            for attribute in (
                "srcset",
                "sizes",
                "width",
                "height",
            ):
                image.attrs.pop(
                    attribute,
                    None,
                )

            counter += 1

        #
        # picture/source srcset
        #
        for source in soup.find_all("source"):

            srcset = source.get("srcset")

            if not srcset:
                continue

            url = srcset.split()[0]

            local = self._download_asset(
                url,
                article.url,
                assets_dir,
                counter,
                logger,
            )

            if not local:
                continue

            source["srcset"] = local

            source.attrs.pop(
                "sizes",
                None,
            )

            counter += 1

        body = soup.body

        if body is None:
            article.html = str(soup)
        else:
            article.html = "".join(
                str(child)
                for child in body.children
            )

    # ------------------------------------------------------------------

    def _download_asset(
        self,
        src: str,
        article_url: str,
        assets_dir: Path,
        counter: int,
        logger=None,
    ) -> str | None:
        """
        Скачать один ресурс.

        Data URI обрабатываются локально,
        остальные ресурсы скачиваются через
        DownloaderService.
        """

        if src.startswith("blob:"):
            return None

        try:

            if src.startswith("data:"):

                data, extension = self._decode_data_uri(
                    src,
                )

            else:

                absolute_url = urljoin(
                    article_url,
                    src,
                )

                extension = self._get_extension(
                    absolute_url,
                )

                data = self._downloader.download_binary(
                    absolute_url,
                )

            filename = (
                f"asset_{counter:03d}.{extension}"
            )

            path = assets_dir / filename

            path.write_bytes(data)

            if logger:

                logger(
                    f"Скачан {filename}"
                )

            return f"assets/{filename}"

        except Exception as exc:

            if logger:

                logger(
                    f"Ошибка загрузки:\n"
                    f"{src}\n"
                    f"{exc}"
                )

            return None

    # ------------------------------------------------------------------

    @staticmethod
    def _decode_data_uri(
        uri: str,
    ) -> tuple[bytes, str]:
        """
        Декодировать Data URI.

        Поддерживает SVG в формах:

            data:image/svg+xml,...
            data:image/svg+xml;base64,...

        Returns
        -------
        tuple[bytes, str]
            Данные ресурса и расширение файла.
        """

        header, data = uri.split(
            ",",
            maxsplit=1,
        )

        if "image/svg+xml" not in header.lower():
            raise ValueError(
                "Поддерживается только SVG Data URI."
            )

        if ";base64" in header.lower():

            content = base64.b64decode(
                data,
            )

        else:

            content = unquote(
                data,
            ).encode(
                "utf-8",
            )

        return content, "svg"

    # ------------------------------------------------------------------

    @staticmethod
    def _get_extension(
        url: str,
    ) -> str:
        """
        Получить расширение ресурса из URL.
        """

        suffix = Path(
            urlparse(url).path
        ).suffix

        if suffix:

            return suffix.lstrip(
                ".",
            )

        return "bin"