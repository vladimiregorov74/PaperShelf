from __future__ import annotations

import importlib

from papershelf.parsers import (
    selectors,
    site_registry,
    site_registry_data,
)
from tools.site_inspector.inspector import SiteInspector


class SiteSupportService:
    """
    Сервис добавления поддержки нового сайта.
    """

    # ------------------------------------------------------------------

    def register(
        self,
        url: str,
        logger,
        source: str | None = None,
        title_suffix: str = "",
    ) -> None:
        """
        Выполнить анализ сайта и зарегистрировать его.
        """

        logger("Запуск анализа сайта...")

        inspector = SiteInspector()

        inspector.load(
            url,
        )

        inspector.inspect(
            source=source,
            title_suffix=title_suffix,
        )

        logger("Перезагрузка конфигурации парсеров...")
        
        importlib.reload(site_registry_data)
        importlib.reload(selectors)
        importlib.reload(site_registry)

        logger("Поддержка сайта успешно добавлена.")