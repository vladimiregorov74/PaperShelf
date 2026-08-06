from __future__ import annotations


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
    ) -> None:
        """
        Parameters
        ----------
        url:
            URL неподдерживаемого сайта.
        """

        self.url = url

        super().__init__(
            f"Сайт не поддерживается: {url}"
        )