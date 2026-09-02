from __future__ import annotations


class HttpFallbackPolicy:
    """
    Определяет, следует ли после ошибки HTTP
    повторить загрузку страницы через BrowserLoader.
    """

    _NOT_FOUND = 404

    # ------------------------------------------------------------------

    def should_use_browser(
        self,
        status_code: int | None,
    ) -> bool:
        """
        Определить необходимость повторной загрузки
        страницы через BrowserLoader.

        Parameters
        ----------
        status_code:
            HTTP-статус ответа сервера.
            Если статус неизвестен, считается,
            что браузер использовать можно.

        Returns
        -------
        bool
            True, если следует попробовать BrowserLoader.
        """

        if status_code is None:
            return True

        return status_code != self._NOT_FOUND