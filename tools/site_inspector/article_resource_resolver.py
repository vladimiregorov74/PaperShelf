from __future__ import annotations

from urllib.parse import urljoin

from bs4 import Tag


# ------------------------------------------------------------------


class ArticleResourceResolver:
    """
    Нормализует URL ресурсов внутри HTML-контейнера статьи.

    Класс отвечает только за преобразование относительных
    URL ресурсов в абсолютные.
    """

    # ------------------------------------------------------------------

    def resolve(
        self,
        element: Tag,
        base_url: str,
    ) -> Tag:
        """
        Нормализовать URL изображений.

        Parameters
        ----------
        element:
            HTML-контейнер статьи.

        base_url:
            URL исходной страницы.

        Returns
        -------
        Tag
            HTML-контейнер с нормализованными URL.
        """

        self._resolve_images(
            element,
            base_url,
        )

        return element

    # ------------------------------------------------------------------

    @staticmethod
    def _resolve_images(
        element: Tag,
        base_url: str,
    ) -> None:
        """
        Преобразовать относительные URL изображений
        в абсолютные.

        Parameters
        ----------
        element:
            HTML-контейнер статьи.

        base_url:
            URL исходной страницы.
        """

        for image in element.find_all(
            "img",
        ):
            src = image.get(
                "src",
            )

            if not src:
                continue

            image["src"] = urljoin(
                base_url,
                src,
            )