from __future__ import annotations

from pathlib import Path

from .models import (
    ArticleCandidate,
    CleaningReport,
)

# ----------------------------------------------------------------------


class SelectorGenerator:
    """
    Генерирует и обновляет файл selectors.py
    для поддерживаемых сайтов.
    """

    # ------------------------------------------------------------------

    def generate(
        self,
        candidate: ArticleCandidate,
        cleaning_report: CleaningReport,
        output_path: Path,
        site_name: str,
    ) -> None:
        """
        Добавить или обновить секцию сайта в selectors.py.

        Parameters
        ----------
        candidate:
            Найденный контейнер статьи.

        cleaning_report:
            Результат анализа очистки контейнера.

        output_path:
            Путь к файлу selectors.py.

        site_name:
            Имя сайта.
        """

        prefix = self._prefix(
            site_name,
        )

        section = self._build_section(
            prefix=prefix,
            selector=candidate.selector,
            cleaning_report=cleaning_report,
            site_name=site_name,
        )

        existing_content = ""

        if output_path.exists():
            existing_content = output_path.read_text(
                encoding="utf-8",
            )

        content = self._update_content(
            existing_content=existing_content,
            section=section,
            prefix=prefix,
        )

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        output_path.write_text(
            content,
            encoding="utf-8",
        )

    # ------------------------------------------------------------------

    @staticmethod
    def _prefix(
        site_name: str,
    ) -> str:
        """
        Преобразовать доменное имя в префикс констант.

        Например:

        metanit.com -> METANIT
        habr.com -> HABR
        """

        name = site_name.split(
            ".",
            1,
        )[0]

        return name.upper()

    # ------------------------------------------------------------------

    @staticmethod
    def _build_section(
        prefix: str,
        selector: str,
        cleaning_report: CleaningReport,
        site_name: str,
    ) -> str:
        """
        Сформировать секцию конкретного сайта.
        """

        remove_selectors = (
            SelectorGenerator._remove_selectors(
                cleaning_report,
            )
        )

        remove_block = (
            SelectorGenerator._format_selectors(
                remove_selectors,
            )
        )

        return f'''# ----------------------------------------------------------------------

# {site_name}

# ----------------------------------------------------------------------

{prefix}_ARTICLE_SELECTORS = (
    "{selector}",
)

{prefix}_CONTENT_SELECTORS = (
    "{selector}",
)

{prefix}_REMOVE_SELECTORS = (
{remove_block})
'''

    # ------------------------------------------------------------------

    @staticmethod
    def _update_content(
        existing_content: str,
        section: str,
        prefix: str,
    ) -> str:
        """
        Добавить или заменить секцию сайта.

        Остальные секции selectors.py остаются без изменений.
        """

        if not existing_content.strip():
            return (
                SelectorGenerator._build_header()
                + section
            )

        start_marker = (
            f"# {prefix.lower()}.com"
        )

        lines = existing_content.splitlines(
            keepends=True,
        )

        section_start = None
        section_end = None

        for index, line in enumerate(lines):

            if line.strip().lower() == start_marker:
                section_start = index - 2

                if section_start < 0:
                    section_start = index

                break

        if section_start is not None:

            for index in range(
                section_start + 1,
                len(lines),
            ):
                line = lines[index]

                if (
                    line.startswith(
                        "# ----------------------------------------------------------------------"
                    )
                    and index > section_start + 1
                ):
                    next_index = index + 1

                    if next_index < len(lines):
                        next_line = lines[next_index].strip()

                        if next_line.startswith("# "):
                            section_end = index
                            break

            if section_end is None:
                section_end = len(lines)

            new_lines = (
                lines[:section_start]
                + [section]
                + lines[section_end:]
            )

            return "".join(
                new_lines,
            )

        content = existing_content.rstrip()

        return (
            content
            + "\n\n"
            + section
        )

    # ------------------------------------------------------------------

    @staticmethod
    def _build_header() -> str:
        """
        Сформировать заголовок selectors.py.
        """

        return '''"""
CSS-селекторы поддерживаемых сайтов.

Если сайт изменит верстку, изменения потребуется
внести только в этот файл.
"""

from __future__ import annotations

'''

    # ------------------------------------------------------------------

    @staticmethod
    def _remove_selectors(
        cleaning_report: CleaningReport,
    ) -> list[str]:
        """
        Получить селекторы элементов,
        которые классифицированы как шум.
        """

        selectors = {
            decision.selector
            for decision in cleaning_report.remove
            if decision.reason != "zero score"
        }

        return sorted(
            selectors,
        )

    # ------------------------------------------------------------------

    @staticmethod
    def _format_selectors(
        selectors: list[str],
    ) -> str:
        """
        Отформатировать CSS-селекторы
        для Python-кортежа.
        """

        return "".join(
            f'    "{selector}",\n'
            for selector in selectors
        )