from __future__ import annotations

from dataclasses import dataclass
from PySide6.QtWidgets import (
    QLineEdit,
    QPushButton,
)
from papershelf.ui.dialogs.base_dialog import BaseDialog
from papershelf.ui.styles.button_styles import (
    SUCCESS_BUTTON_STYLE,
    SECONDARY_BUTTON_STYLE,
)


@dataclass(slots=True)
class NewSiteData:
    """
    Данные регистрации нового сайта.
    """

    source: str
    title_suffix: str

# ------------------------------------------------------------

class NewSiteDialog(BaseDialog):
    """
    Диалог регистрации нового сайта.
    """


    def __init__(
        self,
        parent,
        source: str,
        title_suffix: str = "",
    ) -> None:

        super().__init__(parent)

        self._accepted = False

        self._create_widgets(
            source,
            title_suffix,
        )

        self._create_layout()
        self._connect_signals()

    # ------------------------------------------------------------------

    def _create_layout(
            self,
    ) -> None:
        """
        Создать компоновку окна.
        """

        self.add_field(
            "Источник",
            self._source_edit,
        )

        self.add_field(
            "Суффикс заголовка",
            self._title_suffix_edit,
        )

        self.main_layout.addWidget(
            self._description,
        )

        self.add_buttons(
            self._ok_button,
            self._cancel_button,
        )

        # ------------------------------------------------------------------

    def _connect_signals(
            self,
    ) -> None:
        """
        Подключить сигналы.
        """

        self._ok_button.clicked.connect(
            self._accept,
        )

        self._cancel_button.clicked.connect(
            self.reject,
        )

    # ------------------------------------------------------------------

    def _accept(
            self,
    ) -> None:
        """
        Подтвердить регистрацию.
        """

        if not self._source_edit.text().strip():
            self._source_edit.setFocus()
            return

        self._accepted = True

        self.accept()

    # ------------------------------------------------------------------

    @staticmethod
    def ask(
            parent,
            source: str,
            title_suffix: str = "",
    ) -> NewSiteData | None:
        """
        Показать диалог регистрации нового сайта.

        Parameters
        ----------
        parent:
            Родительское окно.

        source:
            Предлагаемое название источника.

        title_suffix:
            Предлагаемый суффикс заголовка.

        Returns
        -------
        NewSiteData | None
            Введенные пользователем данные либо None,
            если регистрация отменена.
        """

        dialog = NewSiteDialog(
            parent=parent,
            source=source,
            title_suffix=title_suffix,
        )

        dialog.exec()

        if not dialog._accepted:
            return None

        return NewSiteData(
            source=dialog._source_edit.text().strip(),
            title_suffix=dialog._title_suffix_edit.text().strip(),
        )