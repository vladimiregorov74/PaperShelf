from __future__ import annotations

import re
from pathlib import Path

from .naming_utils import domain_prefix, guess_source_name

# ------------------------------------------------------------------


class SiteRegistryGenerator:
    """
    Генерирует и обновляет site_registry_data.py — ЧИСТЫЕ данные
    (домен/источник/суффикс заголовка на сайт), без какого-либо
    "клея". Реальная сборка SiteConfig (_build_config/SITE_CONFIGS)
    живёт в site_registry.py — том, что человек может захотеть
    доработать руками — и этот файл инструмент никогда не трогает,
    он лишь импортирует _SITES из site_registry_data.py.

    Работает по тому же принципу, что и SelectorGenerator для
    selectors.py: добавляет или заменяет ОДНУ строку конкретного
    сайта (по префиксу), остальные строки не трогает.
    """

    # ------------------------------------------------------------------

    def generate(
        self,
        domain: str,
        output_path: Path,
        source: str | None = None,
        title_suffix: str = "",
    ) -> None:
        """
        Добавить или обновить запись сайта в site_registry_data.py.

        Parameters
        ----------
        domain:
            Домен сайта (например "metanit.com", "dan-it.com.ua").

        output_path:
            Путь к site_registry_data.py.

        source:
            Отображаемое имя источника. Если не передано — подбирается
            автоматически по домену (guess_source_name).

        title_suffix:
            Суффикс, отрезаемый от <title> страницы (например
            " / Хабр"). Детектор не может определить его сам — это
            вопрос брендинга конкретного сайта, а не структуры DOM.
        """

        prefix = domain_prefix(
            domain,
        )

        resolved_source = (
            source
            if source is not None
            else guess_source_name(domain)
        )

        new_line = (
            f'    ("{prefix}", "{domain}", '
            f'"{resolved_source}", "{title_suffix}"),\n'
        )

        existing_content = ""

        if output_path.exists():
            existing_content = output_path.read_text(
                encoding="utf-8",
            )

        content = self._update_content(
            existing_content=existing_content,
            prefix=prefix,
            new_line=new_line,
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
    def _update_content(
        existing_content: str,
        prefix: str,
        new_line: str,
    ) -> str:
        """
        Заменить существующую строку сайта (по префиксу) на новую,
        либо добавить новую перед закрывающей скобкой кортежа _SITES.
        Файл теперь содержит ТОЛЬКО данные (никакого "клея" после
        _SITES не бывает) — поэтому, в отличие от старой версии,
        писавшей в site_registry.py, никакой хвост защищать не нужно:
        закрывающая скобка ")" — это всегда самый конец файла.
        """

        if not existing_content.strip():
            return (
                SiteRegistryGenerator._build_header()
                + new_line
                + ")\n"
            )

        lines = existing_content.splitlines(
            keepends=True,
        )

        entry_pattern = re.compile(
            r'^\s*\(\s*"' + re.escape(prefix) + r'"\s*,'
        )

        for index, line in enumerate(lines):

            if entry_pattern.match(line):
                lines[index] = new_line
                return "".join(lines)

        for index, line in enumerate(lines):

            if line.rstrip("\n") == ")":
                lines.insert(
                    index,
                    new_line,
                )
                return "".join(lines)

        return (
            existing_content.rstrip("\n")
            + "\n"
            + new_line
        )

    # ------------------------------------------------------------------

    @staticmethod
    def _build_header() -> str:
        """
        Сформировать заголовок нового site_registry_data.py.
        """

        return (
            '"""\n'
            "Данные реестра сайтов — ЧИСТЫЕ данные, без кода.\n"
            "\n"
            "НЕ РЕДАКТИРУЙТЕ ВРУЧНУЮ — перезаписывается целиком при\n"
            "каждом запуске tools/inspect_site.py <url> (по префиксу\n"
            "сайта, остальные строки не трогаются). Логика сборки\n"
            "SiteConfig из этих данных — в site_registry.py, который\n"
            "инструмент никогда не переписывает.\n"
            '"""\n'
            "\n"
            "from __future__ import annotations\n"
            "\n"
            "_SITES: tuple[tuple[str, str, str, str], ...] = (\n"
        )
