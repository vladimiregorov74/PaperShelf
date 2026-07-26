from __future__ import annotations

from PySide6.QtWidgets import QLineEdit


class UrlWidget(QLineEdit):
	"""Поле ввода URL."""

	def __init__(self) -> None:
		super().__init__()

		self._configure()

	def _configure(self) -> None:
		self.setPlaceholderText("https://")

		self.setClearButtonEnabled(True)

		self.setMinimumHeight(38)

	def url(self) -> str:
		return self.text().strip()