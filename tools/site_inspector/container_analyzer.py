from __future__ import annotations

from pathlib import PurePosixPath
from urllib.parse import urlparse

from bs4 import Tag

from .models import (
    ChildInfo,
    ContainerAnalysis,
    HeadingInfo, ImageInfo, TableInfo, CodeBlockInfo, LinkInfo,
)
from .constants import (
    CODE_WEIGHT,
    HEADING_WEIGHT,
    IMAGE_WEIGHT,
    LINK_WEIGHT,
    PARAGRAPH_WEIGHT,
    POSITIVE_CLASSES,
    NEGATIVE_CLASSES,
    TABLE_WEIGHT,
    TEXT_WEIGHT, LANGUAGE_ALIASES, LANGUAGE_PREFIXES,
)

# ------------------------------------------------------------------


class ContainerAnalyzer:
    """
    Выполняет подробный анализ HTML-контейнера.
    """

    # ------------------------------------------------------------------
    
    # ------------------------------------------------------------------
    
    def analyze(
            self,
            element: Tag,
    ) -> ContainerAnalysis:
        """
        Выполнить подробный анализ контейнера.

        Parameters
        ----------
        element:
            HTML-контейнер BeautifulSoup.

        Returns
        -------
        ContainerAnalysis
        """
        
        return ContainerAnalysis(
            selector=self._selector(
                element,
            ),
            
            children=self._children(
                element,
            ),
            
            headings=self._headings(
                element,
            ),
            
            images=self._images(
                element,
            ),
            
            tables=self._tables(
                element,
            ),
            
            code_blocks=self._code_blocks(
                element,
            ),
            
            links=self._links(
                element,
            ),
            
            classes=self._class_statistics(
                element,
            ),
        )

    # ------------------------------------------------------------------

    def _children(
            self,
            element: Tag,
    ) -> list[ChildInfo]:
        """
        Получить дочерние элементы первого уровня.

        Parameters
        ----------
        element:
            HTML-контейнер.

        Returns
        -------
        list[ChildInfo]
        """

        children: list[ChildInfo] = []

        for child in element.find_all(
                recursive=False,
        ):

            if not isinstance(
                    child,
                    Tag,
            ):
                continue

            text = child.get_text(
                " ",
                strip=True,
            )

            info = ChildInfo(
                tag=child.name,

                selector=self._selector(
                    child,
                ),

                css_id=child.get(
                    "id",
                    "",
                ),

                css_classes=child.get(
                    "class",
                    [],
                ),

                text_length=len(text),

                paragraphs=len(
                    child.find_all(
                        "p",
                    )
                ),

                headings=len(
                    child.find_all(
                        [
                            "h1",
                            "h2",
                            "h3",
                            "h4",
                            "h5",
                            "h6",
                        ]
                    )
                ),

                images=len(
                    child.find_all(
                        "img",
                    )
                ),

                code_blocks=len(
                    child.find_all(
                        [
                            "pre",
                            "code",
                        ]
                    )
                ),

                tables=len(
                    child.find_all(
                        "table",
                    )
                ),

                links=len(
                    child.find_all(
                        "a",
                    )
                ),
            )
            info.score = self._score_child(
                info,
            )
            children.append(
                info,
            )

        return children

    # ------------------------------------------------------------------

    # ------------------------------------------------------------------

    def _headings(
            self,
            element: Tag,
    ) -> list[HeadingInfo]:
        """
        Собрать информацию о заголовках контейнера.

        Parameters
        ----------
        element:
            HTML-контейнер.

        Returns
        -------
        list[HeadingInfo]
        """

        headings: list[HeadingInfo] = []

        for tag in element.find_all(
                [
                    "h1",
                    "h2",
                    "h3",
                    "h4",
                    "h5",
                    "h6",
                ]
        ):
            headings.append(
                HeadingInfo(
                    level=int(tag.name[1]),
                    text=tag.get_text(strip=True,),
                    selector=self._selector(tag,),
                )
            )

        return headings

    # ------------------------------------------------------------------

    def _images(
            self,
            element: Tag,
    ) -> list[ImageInfo]:
        """
        Собрать информацию об изображениях контейнера.

        Parameters
        ----------
        element:
            HTML-контейнер.

        Returns
        -------
        list[ImageInfo]
        """

        images: list[ImageInfo] = []

        for tag in element.find_all("img"):
            src = tag.get(
                "src",
                "",
            )

            images.append(
                ImageInfo(
                    src=src,
                    alt=tag.get(
                        "alt",
                        "",
                    ),
                    extension=self._extension(
                        src,
                    ),
                )
            )

        return images

    # ------------------------------------------------------------------

    def _tables(
            self,
            element: Tag,
    ) -> list[TableInfo]:
        """
        Собрать информацию о таблицах контейнера.

        Parameters
        ----------
        element:
            HTML-контейнер.

        Returns
        -------
        list[TableInfo]
        """

        tables: list[TableInfo] = []

        for table in element.find_all(
                "table",
        ):

            rows = table.find_all(
                "tr",
            )

            columns = 0

            if rows:
                columns = max(
                    len(
                        row.find_all(
                            [
                                "td",
                                "th",
                            ]
                        )
                    )
                    for row in rows
                )

            tables.append(
                TableInfo(
                    rows=len(rows),

                    columns=columns,

                    css_classes=table.get(
                        "class",
                        [],
                    ),
                )
            )

        return tables

    # ------------------------------------------------------------------

    # ------------------------------------------------------------------

    def _code_blocks(
            self,
            element: Tag,
    ) -> list[CodeBlockInfo]:
        """
        Собрать информацию о блоках кода контейнера.

        Parameters
        ----------
        element:
            HTML-контейнер.

        Returns
        -------
        list[CodeBlockInfo]
        """

        blocks: list[CodeBlockInfo] = []

        for tag in element.find_all(
                [
                    "pre",
                    "code",
                ]
        ):
            text = tag.get_text(
                "\n",
                strip=True,
            )

            classes = tag.get(
                "class",
                [],
            )

            language = self._detect_language(
                classes,
            )

            blocks.append(
                CodeBlockInfo(
                    tag=tag.name,

                    language=language,

                    classes=classes,

                    lines=len(
                        text.splitlines()
                    ),

                    text=text,
                )
            )

        return blocks

    # ------------------------------------------------------------------

    def _links(
            self,
            element: Tag,
    ) -> list[LinkInfo]:
        """
        Собрать информацию о ссылках контейнера.

        Parameters
        ----------
        element:
            HTML-контейнер.

        Returns
        -------
        list[LinkInfo]
        """

        links: list[LinkInfo] = []

        for tag in element.find_all(
                "a",
        ):
            href = tag.get(
                "href",
                "",
            )

            text = tag.get_text(
                " ",
                strip=True,
            )

            links.append(
                LinkInfo(
                    href=href,

                    text=text,

                    external=(
                            href.startswith("http://")
                            or href.startswith("https://")
                    ),
                )
            )

        return links

    # ------------------------------------------------------------------

    def _class_statistics(
            self,
            element: Tag,
    ) -> dict[str, int]:
        """
        Подсчитать частоту использования CSS-классов
        внутри контейнера.

        Parameters
        ----------
        element:
            HTML-контейнер.

        Returns
        -------
        dict[str, int]
        """

        statistics: dict[str, int] = {}

        for tag in element.find_all(True):

            for css_class in tag.get(
                    "class",
                    [],
            ):
                statistics[css_class] = (
                        statistics.get(
                            css_class,
                            0,
                        ) + 1
                )

        return dict(
            sorted(
                statistics.items(),
                key=lambda item: (
                    -item[1],
                    item[0],
                ),
            )
        )
    
    # ------------------------------------------------------------------
    
    def _selector(
            self,
            element: Tag,
    ) -> str:
        """
        Построить CSS-селектор элемента.

        Parameters
        ----------
        element:
            HTML-элемент BeautifulSoup.

        Returns
        -------
        str
            CSS-селектор.
        """
        
        selector = element.name
        
        css_id = element.get("id")
        
        if css_id:
            selector += f"#{css_id}"
        
        css_classes = element.get("class", [])
        
        if css_classes:
            selector += "".join(
                f".{css_class}"
                for css_class in css_classes
            )
        
        return selector

    # ------------------------------------------------------------------

    def _score_child(
            self,
            child: ChildInfo,
    ) -> float:
        """
        Вычислить оценку дочернего контейнера.

        Parameters
        ----------
        child:
            Информация о дочернем контейнере.

        Returns
        -------
        float
        """



        score = 0.0

        score += child.text_length * TEXT_WEIGHT

        score += child.paragraphs * PARAGRAPH_WEIGHT

        score += child.headings * HEADING_WEIGHT

        score += child.images * IMAGE_WEIGHT

        score += child.code_blocks * CODE_WEIGHT

        score += child.tables * TABLE_WEIGHT

        score += child.links * LINK_WEIGHT

        for css_class in child.css_classes:
            css_class = css_class.lower()

            score += POSITIVE_CLASSES.get(
                css_class,
                0,
            )

            score += NEGATIVE_CLASSES.get(
                css_class,
                0,
            )

        return score

    # ------------------------------------------------------------------

    @staticmethod
    def _extension(path: str) -> str:
        """
        Получить расширение файла.

        Parameters
        ----------
        path:
            URL изображения.

        Returns
        -------
        str
        """

        parsed = urlparse(path)

        suffix = PurePosixPath(
            parsed.path,
        ).suffix

        return suffix.removeprefix(".").lower()

    # ------------------------------------------------------------------

    @classmethod
    def _detect_language(
            cls,
            classes: list[str],
    ) -> str:
        """
        Определить язык программирования по CSS-классам.

        Parameters
        ----------
        classes:
            CSS-классы элемента.

        Returns
        -------
        str
            Название языка или пустая строка.
        """

        for css_class in classes:

            css_class = css_class.lower()

            # Точное совпадение
            language = LANGUAGE_ALIASES.get(css_class)

            if language:
                return language

            # Поиск по известным префиксам
            for prefix in LANGUAGE_PREFIXES:

                if not css_class.startswith(prefix):
                    continue

                language = css_class.removeprefix(prefix)

                language = language.rstrip(";")

                return LANGUAGE_ALIASES.get(
                    language,
                    language,
                )

        return ""