from __future__ import annotations

from .constants import REPORT_WIDTH
from .models import (
    ChildInfo,
    ContainerAnalysis,
    ContainerInfo,
    InspectionReport,
)

class ReportFormatter:
    """
    Форматирование отчета SiteInspector.
    """

    # ------------------------------------------------------------------

    @classmethod
    def format(
        cls,
        report: InspectionReport,
    ) -> str:
        """
        Преобразовать отчет в текст.

        Parameters
        ----------
        report:
            Отчет инспектора.

        Returns
        -------
        str
        """

        sections = [
            cls._page(report),
            cls._statistics(report),
            cls._containers(report),]
        if report.article_candidate is not None:
            sections.append(
                cls._analysis(
                    report.article_candidate.analysis,
                )
            )
        sections.append(
                cls._suggestion(report),
            )

        return "\n\n".join(sections)

    # ------------------------------------------------------------------

    @staticmethod
    def _header(
        title: str,
    ) -> str:
        """
        Построить заголовок раздела.

        Parameters
        ----------
        title:
            Название раздела.

        Returns
        -------
        str
        """

        line = "=" * REPORT_WIDTH

        return (
            f"{line}\n"
            f"{title}\n"
            f"{line}"
        )

    # ------------------------------------------------------------------

    @classmethod
    def _page(
        cls,
        report: InspectionReport,
    ) -> str:
        """
        Построить раздел с информацией о странице.
        """

        page = report.page

        return "\n".join(
            [
                cls._header("PAGE"),
                "",
                f"Title    : {page.title}",
                f"URL      : {page.url}",
                f"Encoding : {page.encoding or '-'}",
            ]
        )

    # ------------------------------------------------------------------

    @classmethod
    def _statistics(
        cls,
        report: InspectionReport,
    ) -> str:
        """
        Построить раздел статистики.
        """

        statistics = report.statistics

        return "\n".join(
            [
                cls._header("STATISTICS"),
                "",
                f"Headings   : {statistics.headings}",
                f"Images     : {statistics.images}",
                f"Code       : {statistics.code_blocks}",
                f"Tables     : {statistics.tables}",
                f"Links      : {statistics.links}",
                f"Containers : {statistics.containers}",
            ]
        )

    # ------------------------------------------------------------------

    @classmethod
    def _containers(
        cls,
        report: InspectionReport,
    ) -> str:
        """
        Построить раздел лучших контейнеров.
        """

        lines = [
            cls._header(
                "BEST CONTAINERS"
            ),
            "",
        ]

        for index, container in enumerate(
            report.containers[:5],
            start=1,
        ):

            classes = " ".join(
                container.css_classes,
            )

            lines.extend(
                [
                    f"#{index}",
                    "",
                    f"Score      : {container.score:.1f}",
                    f"Tag        : {container.tag}",
                    f"Id         : {container.css_id or '-'}",
                    f"Classes    : {classes or '-'}",
                    f"Text       : {container.text_length}",
                    f"Paragraphs : {container.paragraphs}",
                    f"Headings   : {container.headings}",
                    f"Images     : {container.images}",
                    f"Code       : {container.code_blocks}",
                    f"Tables     : {container.tables}",
                    f"Links      : {container.links}",
                    "",
                    "-" * REPORT_WIDTH,
                    "",
                ]
            )

        return "\n".join(lines)

    # ------------------------------------------------------------------

    @classmethod
    def _suggestion(
        cls,
        report: InspectionReport,
    ) -> str:
        """
        Построить рекомендации по выбору контейнера статьи.
        """

        lines = [
            cls._header(
                "SUGGESTED ARTICLE CONTAINER"
            ),
            "",
        ]
        
        candidate = report.article_candidate
        
        if candidate is None:
            lines.append(
                "Container not found."
            )
            
            return "\n".join(lines)

        selector = candidate.selector

        lines.extend(
            [
                f"Selector : {selector}",
                
                "",
                "Parser:",
                "",
                "ARTICLE_SELECTOR = (",
                f'    "{selector}",',
                ")",
            ]
        )

        return "\n".join(lines)

    # ------------------------------------------------------------------

    @staticmethod
    def _build_selector(
        container: ContainerInfo,
    ) -> str:
        """
        Построить CSS-селектор контейнера.
        """

        selector = container.tag

        if container.css_id:

            selector += (
                f"#{container.css_id}"
            )

        for css_class in container.css_classes:

            selector += (
                f".{css_class}"
            )

        return selector

    # ------------------------------------------------------------------

    @classmethod
    def _analysis(
            cls,
            analysis: ContainerAnalysis,
    ) -> str:
        """
        Построить анализ лучшего контейнера.
        """

        lines = [
            cls._header(
                "CONTAINER ANALYSIS",
            ),
            "",
            f"Selector : {analysis.selector}",
            "",
            "Children",
            "",
        ]

        if not analysis.children:
            lines.append(
                "No child containers."
            )

            return "\n".join(lines)

        lines.append(
            (
                f"{'Score':>7}  "
                f"{'Selector':<35}"
                f"{'Text':>8}"
                f"{'P':>5}"
                f"{'H':>5}"
                f"{'Img':>5}"
                f"{'Code':>6}"
                f"{'Tbl':>5}"
                f"{'Link':>6}"
            )
        )

        lines.append(
            "-" * REPORT_WIDTH
        )

        for child in analysis.children:
            lines.append(
                cls._child_row(
                    child,
                )
            )

        return "\n".join(lines)

    # ------------------------------------------------------------------

    @staticmethod
    def _child_row(
            child: ChildInfo,
    ) -> str:
        """
        Построить строку таблицы дочернего контейнера.
        """

        return (
            f"{child.score:7.1f}  "
            f"{child.selector:<35}"
            f"{child.text_length:>8}"
            f"{child.paragraphs:>5}"
            f"{child.headings:>5}"
            f"{child.images:>5}"
            f"{child.code_blocks:>6}"
            f"{child.tables:>5}"
            f"{child.links:>6}"
        )