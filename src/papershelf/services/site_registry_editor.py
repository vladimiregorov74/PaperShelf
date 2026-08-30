from __future__ import annotations

import importlib

from papershelf.core.paths import SITE_REGISTRY_DATA_FILE, SELECTORS_FILE
from papershelf.registry.registry_file_editor import RegistryFileEditor
from papershelf.registry.selector_file_editor import SelectorFileEditor


class SiteRegistryEditor:
    """
    Редактирование списка поддерживаемых сайтов.
    """

    # ------------------------------------------------------------------

    def __init__(self) -> None:

        self._registry = RegistryFileEditor(SITE_REGISTRY_DATA_FILE)

        self._selectors = SelectorFileEditor(SELECTORS_FILE)
        
    # ------------------------------------------------------------------

    def remove(
        self,
        identifier: str,
    ) -> None:
        """
        Полностью удалить поддержку сайта.

        Parameters
        ----------
        identifier:
            Идентификатор сайта.
        """
        
        self._registry.remove(
            identifier,
        )
        
        self._selectors.remove(
            identifier,
        )
        
        self._reload_modules()
    # ------------------------------------------------------------------
    
    def _reload_modules(self,) -> None:
        """
        Перезагрузить конфигурацию сайтов.
        """
        
        from papershelf.parsers import (
            selectors,
            site_registry,
            site_registry_data,
        )
        
        importlib.reload(
            site_registry_data,
        )
        
        importlib.reload(
            selectors,
        )
        
        importlib.reload(
            site_registry,
        )
        
   
    # ------------------------------------------------------------------

    def _remove_selectors(
        self,
        identifier: str,
    ) -> None:
        """
        Удалить CSS-селекторы сайта.
        """

        raise NotImplementedError
    
   