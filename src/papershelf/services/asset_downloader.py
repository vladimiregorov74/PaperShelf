from __future__ import annotations

from pathlib import Path
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup

from papershelf.models import Article
from papershelf.services.downloader import DownloaderService


class AssetDownloader:
    """
    Скачивает ресурсы статьи.

    Пока поддерживаются:

    - img[src]
    - source[srcset]

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
        """

        if src.startswith("data:"):
            return None

        if src.startswith("blob:"):
            return None

        absolute_url = urljoin(
            article_url,
            src,
        )

        try:

            extension = self._get_extension(
                absolute_url,
            )

            filename = (
                f"asset_{counter:03d}.{extension}"
            )

            data = self._downloader.download_binary(
                absolute_url,
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
                    f"{absolute_url}\n"
                    f"{exc}"
                )

            return None

    # ------------------------------------------------------------------

    @staticmethod
    def _get_extension(
        url: str,
    ) -> str:

        suffix = Path(
            urlparse(url).path
        ).suffix

        if suffix:

            return suffix.lstrip(".")

        return "bin"