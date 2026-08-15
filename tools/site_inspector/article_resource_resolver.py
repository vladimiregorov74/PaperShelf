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

        Учитывает ленивую (lazy) загрузку картинок: многие сайты
        кладут в src крошечную заглушку (прозрачный gif / 1x1
        base64-SVG), а настоящий адрес — в отдельном data-*-
        атрибуте. Название атрибута отличается от библиотеки к
        библиотеке (data-src, data-original, data-lazy-src,
        data-zzload-source-img и т.п.), но почти всегда содержит
        "src" — по этому и ищем, не завязываясь на конкретное имя.

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
            src = ArticleResourceResolver._real_src(
                image,
            )

            if not src:
                continue

            image["src"] = urljoin(
                base_url,
                src,
            )

    # ------------------------------------------------------------------

    @staticmethod
    def _real_src(
        image: Tag,
    ) -> str | None:
        """
        Найти реальный URL картинки среди атрибутов тега.

        Приоритет: любой атрибут (кроме самого src и *srcset —
        у него другой, многозначный формат "url 1x, url 2x"),
        чьё имя содержит "src" и чьё значение не выглядит data:
        URI-заглушкой. Если такого нет — используется обычный src
        (даже если это data: URI — резолвить всё равно нечего
        другое).

        Parameters
        ----------
        image:
            Тег <img>.

        Returns
        -------
        str | None
        """

        for attr_name, attr_value in image.attrs.items():

            if attr_name == "src":
                continue

            if not isinstance(attr_value, str):
                continue

            lowered = attr_name.lower()

            if "srcset" in lowered:
                continue

            if "src" not in lowered and "source" not in lowered:
                continue

            if not attr_value or attr_value.startswith("data:"):
                continue

            return attr_value

        return image.get(
            "src",
        )