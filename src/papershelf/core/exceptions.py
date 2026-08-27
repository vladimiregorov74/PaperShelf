from __future__ import annotations

from papershelf.models.loaded_page import LoadedPage


class PaperShelfError(Exception):
    """
    Базовое исключение приложения.
    """


# ------------------------------------------------------------------


class UnsupportedSiteError(PaperShelfError):
    """
    Сайт не поддерживается приложением.
    """

    # ------------------------------------------------------------------

    def __init__(
        self,
        url: str,
        page: LoadedPage | None = None,
    ) -> None:
        """
        Parameters
        ----------
        url:
            URL неподдерживаемого сайта.

        page:
            Уже загруженная страница, если она доступна.
        """

        self.url = url
        self.page = page

        super().__init__(
            f"Сайт не поддерживается: {url}"
        )


# ------------------------------------------------------------------


class SiteAnalysisError(PaperShelfError):
    """
    Не удалось автоматически определить структуру сайта.
    """

    # ------------------------------------------------------------------

    def __init__(
        self,
        url: str,
        reason: str,
    ) -> None:

        self.url = url
        self.reason = reason

        super().__init__(
            reason,
        )


# ------------------------------------------------------------------


class DynamicSiteError(PaperShelfError):
    """
    Страница формируется JavaScript и не может быть
    проанализирована обычной загрузкой HTML.
    """

    # ------------------------------------------------------------------

    def __init__(
        self,
        url: str,
    ) -> None:

        self.url = url

        super().__init__(
            "Сайт использует динамическую загрузку содержимого (JavaScript). "
            "Автоматический анализ невозможен."
        )


# ------------------------------------------------------------------


class EmptyPageError(PaperShelfError):
    """
    Страница не содержит полезного HTML.
    """

    # ------------------------------------------------------------------

    def __init__(
        self,
        url: str,
    ) -> None:

        self.url = url

        super().__init__(
            "Получена пустая или некорректная HTML-страница."
        )