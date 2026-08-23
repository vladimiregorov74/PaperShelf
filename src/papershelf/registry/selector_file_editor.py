from __future__ import annotations

from pathlib import Path


class SelectorFileEditor:
    """
    Редактор selectors.py.
    """

    # ------------------------------------------------------------------

    def __init__(
        self,
        path: Path,
    ) -> None:

        self._path = path

    # ------------------------------------------------------------------

    def remove(
            self,
            identifier: str,
    ) -> None:
        """
        Удалить блок селекторов сайта.
        """

        lines = self._path.read_text(
            encoding="utf-8",
        ).splitlines()

        lines = self._remove_block(
            lines,
            identifier,
        )

        self._path.write_text(
            "\n".join(lines) + "\n",
            encoding="utf-8",
        )

    # ------------------------------------------------------------------

    def _remove_block(
            self,
            lines: list[str],
            identifier: str,
    ) -> list[str]:
        """
        Удалить блок сайта.
        """

        prefix = f"{identifier}_AUTHOR_SELECTORS"

        start = None

        for index, line in enumerate(lines):

            if line.startswith(prefix):
                start = index
                break

        if start is None:
            return lines

        return self._cut_block(
            lines,
            start,
        )

    # ------------------------------------------------------------------

    def _cut_block(
            self,
            lines: list[str],
            start: int,
    ) -> list[str]:
        """
        Вырезать блок сайта.
        """

        end = start

        selectors_found = 0

        while end < len(lines):

            if lines[end].endswith("_SELECTORS = ("):
                selectors_found += 1

            if (
                    selectors_found == 4
                    and lines[end] == ")"
            ):
                break

            end += 1

        #
        # Захватываем последние строки.
        #

        end += 1

        #
        # И пустые строки после блока.
        #

        while (
                end < len(lines)
                and lines[end].strip() == ""
        ):
            end += 1

        #
        # Комментарии перед блоком.
        #

        start_comment = start

        while (
                start_comment > 0
                and (
                        lines[start_comment - 1].startswith("#")
                        or lines[start_comment - 1].strip() == ""
                )
        ):
            start_comment -= 1

        return (
                lines[:start_comment]
                + lines[end:]
        )