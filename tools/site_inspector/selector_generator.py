from __future__ import annotations

from pathlib import Path

from .models import (
    ArticleCandidate,
    CleaningReport,
)
from .naming_utils import domain_prefix

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
        author_selectors: list[str] | None = None,
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

        author_selectors:
            Селекторы-кандидаты блока автора. Может быть пустым,
            если на странице автор не указан или не найден.
        """

        prefix = self._prefix(
            site_name,
        )

        section = self._build_section(
            prefix=prefix,
            selector=candidate.selector,
            cleaning_report=cleaning_report,
            site_name=site_name,
            author_selectors=author_selectors or [],
        )

        existing_content = ""

        if output_path.exists():
            existing_content = output_path.read_text(
                encoding="utf-8",
            )

        content = self._update_content(
            existing_content=existing_content,
            section=section,
            site_name=site_name,
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
        dan-it.com.ua -> DAN_IT
        """

        return domain_prefix(
            site_name,
        )

    # ------------------------------------------------------------------

    @staticmethod
    def _build_section(
        prefix: str,
        selector: str,
        cleaning_report: CleaningReport,
        site_name: str,
        author_selectors: list[str],
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

        author_block = (
            SelectorGenerator._format_selectors(
                author_selectors,
            )
        )

        return f'''# ----------------------------------------------------------------------

# {site_name}

# ----------------------------------------------------------------------

{prefix}_AUTHOR_SELECTORS = (
{author_block})

{prefix}_ARTICLE_SELECTORS = (
    {selector!r},
)

{prefix}_CONTENT_SELECTORS = (
    {selector!r},
)

{prefix}_REMOVE_SELECTORS = (
{remove_block})
'''

    # ------------------------------------------------------------------

    @staticmethod
    def _update_content(
        existing_content: str,
        section: str,
        site_name: str,
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

        # Маркер строится из того же site_name, что и заголовок
        # секции в _build_section (f"# {site_name}") — раньше здесь
        # реконструировали "# {prefix.lower()}.com" с ЖЁСТКО
        # зашитым ".com", из-за чего секция для любого не-.com домена
        # (wezom.academy, dan-it.com.ua) никогда не находилась и
        # дописывалась заново при каждом запуске вместо замены.
        start_marker = (
            f"# {site_name.lower()}"
        )

        lines = existing_content.splitlines(
            keepends=True,
        )

        section_start = None

        for index, line in enumerate(lines):

            if line.strip().lower() == start_marker:
                section_start = index - 2

                if section_start < 0:
                    section_start = index

                break

        if section_start is not None:

            # Заголовок КАЖДОЙ секции — фиксированный шаблон
            # ровно из 5 строк (см. _build_section):
            #   dash, пусто, "# site", пусто, dash
            # Следующая секция (если есть) может начинаться только
            # ПОСЛЕ этого фиксированного заголовка текущей секции —
            # ищем следующую dash-строку начиная оттуда, а не сразу
            # после section_start (где первой встретится ВТОРОЙ dash
            # этой же секции, а не начало следующей).
            search_from = section_start + 5

            section_end = len(
                lines,
            )

            dash_line = (
                "# ----------------------------------------------------------------------\n"
            )

            for index in range(
                search_from,
                len(lines),
            ):

                if lines[index] == dash_line:
                    section_end = index
                    break

            new_lines = (
                lines[:section_start]
                + [section]
                + (
                    ["\n"]
                    if section_end < len(lines)
                    else []
                )
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

        Используем repr(), а не f'"{selector}"' — некоторые селекторы
        сами содержат двойные кавычки (например 'meta[name="author"]'
        из ArticleAuthorDetector), и наивная обёртка в "..." ломает
        сгенерированный файл (SyntaxError при импорте selectors.py).
        repr() сам выбирает безопасные кавычки и экранирование.
        """

        return "".join(
            f'    {selector!r},\n'
            for selector in selectors
        )