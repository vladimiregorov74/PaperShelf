from __future__ import annotations

import importlib
from urllib.parse import urlparse

from papershelf.core.exceptions import SiteAnalysisError
from papershelf.core.paths import SELECTORS_FILE, SITE_REGISTRY_DATA_FILE
from papershelf.parsers import (
    selectors,
    site_registry,
    site_registry_data,
)
from tools.site_inspector.inspector import SiteInspector
from tools.site_inspector.selector_generator import SelectorGenerator
from tools.site_inspector.site_registry_generator import SiteRegistryGenerator


class SiteSupportService:
    """
    Сервис добавления поддержки нового сайта.
    """

    # ------------------------------------------------------------------

    def __init__(self) -> None:

        self._selector_generator = (
            SelectorGenerator()
        )

        self._site_registry_generator = (
            SiteRegistryGenerator()
        )

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
        logger(f"URL анализа: {url}")
        
        inspector = SiteInspector()
        
        inspector.load(url)
        
        report = inspector.inspect(
            source=source,
            title_suffix=title_suffix,
        )
        
        if report.article_candidate is None:
            raise SiteAnalysisError(
                url=url,
                reason=(
                    "Не удалось автоматически определить "
                    "контейнер статьи."
                ),
            )
        
        logger("Запись selectors.py...")
        
        self._selector_generator.generate(
            candidate=report.article_candidate,
            cleaning_report=report.cleaning_report,
            author_selectors=report.author_selectors,
            output_path=SELECTORS_FILE,
            site_name=urlparse(
                url,
            ).netloc,
        )
        
        logger("Запись site_registry_data.py...")
        
        self._site_registry_generator.generate(
            domain=urlparse(
                url,
            ).netloc,
            output_path=SITE_REGISTRY_DATA_FILE ,
            source=source,
            title_suffix=title_suffix,
        )
        
        logger("Перезагрузка конфигурации парсеров...")
        
        importlib.reload(site_registry_data)
        importlib.reload(selectors)
        importlib.reload(site_registry)
        
        logger("Поддержка сайта успешно добавлена.")