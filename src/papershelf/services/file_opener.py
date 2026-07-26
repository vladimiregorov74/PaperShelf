from __future__ import annotations

import platform
import subprocess
from pathlib import Path


class FileOpener:
    """
    Открытие файлов и каталогов средствами ОС.
    """

    # ------------------------------------------------------------------

    @staticmethod
    def open_directory(
        directory: Path,
    ) -> None:
        """
        Открыть каталог.
        """

        system = platform.system()

        if system == "Windows":

            subprocess.Popen(
                [
                    "explorer",
                    str(directory),
                ]
            )

            return

        if system == "Darwin":

            subprocess.Popen(
                [
                    "open",
                    str(directory),
                ]
            )

            return

        subprocess.Popen(
            [
                "xdg-open",
                str(directory),
            ]
        )