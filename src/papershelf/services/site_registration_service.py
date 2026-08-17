from __future__ import annotations

from PySide6.QtWidgets import QWidget

from papershelf.core.exceptions import UnsupportedSiteError
from papershelf.ui.dialogs.confirm_dialog import ConfirmDialog


# ----------------------------------------------------------------------


class SiteRegistrationService:
    """
    Регистрация новых сайтов.

    Если сайт не поддерживается, предлагает пользователю
    выполнить автоматический анализ.
    """

    # ------------------------------------------------------------------

    def ensure_registered(
        self,
        url: str,
        parent: QWidget | None = None,
    ) -> None:
        """
        Убедиться, что сайт зарегистрирован.

        Parameters
        ----------
        url:
            URL статьи.

        parent:
            Родительское окно.

        Raises
        ------
        UnsupportedSiteError
            Если пользователь отказался выполнять анализ.
        """

        dialog = ConfirmDialog(
            title="Новый сайт",
            message=(
                "Этот сайт пока не поддерживается.\n\n"
                "Выполнить автоматический анализ?"
            ),
            parent=parent,
        )

        if not dialog.exec():
            raise UnsupportedSiteError(url)

        #
        # Пока здесь ничего.
        # Следующим этапом сюда встроим SiteInspector.
        #