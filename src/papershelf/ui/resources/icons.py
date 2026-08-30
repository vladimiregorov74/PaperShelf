from __future__ import annotations

from pathlib import Path

from PySide6.QtGui import QIcon


_ICON_DIRECTORY = (
    Path(__file__).parent
    
    / "icons"
)


# ------------------------------------------------------------------


def icon(
    name: str,
) -> QIcon:
    """
    Загрузить SVG-иконку.

    Parameters
    ----------
    name:
        Имя файла без расширения.

    Returns
    -------
    QIcon
        Загруженная иконка.
    """
   
    return QIcon(
        str(
            _ICON_DIRECTORY / f"{name}.svg"
        )
    )