from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel


class PreviewWidget(QLabel):
    """Область предварительного просмотра."""

    def __init__(self) -> None:
        super().__init__()

        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setText("Предварительный просмотр")