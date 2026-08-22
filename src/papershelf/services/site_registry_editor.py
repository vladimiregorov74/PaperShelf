from __future__ import annotations

import ast
import importlib
from pathlib import Path

from papershelf.core.paths import SITE_REGISTRY_DATA_FILE, SELECTORS_FILE
from papershelf.parsers import site_registry_data
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
        
    # # ------------------------------------------------------------------
    #
    # def _remove_registry(
    #         self,
    #         identifier: str,
    # ) -> None:
    #     """
    #     Удалить запись из реестра.
    #     """
    #
    #     sites = self._load_sites()
    #
    #     sites = [
    #         site
    #         for site in sites
    #         if site[0] != identifier
    #     ]
    #
    #     self._save_sites(
    #         sites,
    #     )

    # ------------------------------------------------------------------

    def _remove_selectors(
        self,
        identifier: str,
    ) -> None:
        """
        Удалить CSS-селекторы сайта.
        """

        raise NotImplementedError
    
    # # ------------------------------------------------------------------
    #
    # def _save_sites(
    #         self,
    #         sites: list[tuple[str, str, str, str]],
    # ) -> None:
    #     """
    #     Записать site_registry_data.py.
    #     """
    #
    #     text = self._format_registry(
    #         sites,
    #     )
    #
    #     self._registry_file.write_text(
    #         text,
    #         encoding="utf-8",
    #     )
    
    # # ------------------------------------------------------------------
    #
    # def _format_registry(
    #         self,
    #         sites: list[tuple[str, str, str, str]],
    # ) -> str:
    #     """
    #     Построить содержимое
    #     site_registry_data.py.
    #     """
    #
    #     lines = [
    #         "from __future__ import annotations",
    #         "",
    #         "_SITES: tuple[tuple[str, str, str, str], ...] = (",
    #         "",
    #     ]
    #
    #     for identifier, domain, source, suffix in sites:
    #         lines.append(
    #             f'    ("{identifier}", "{domain}", "{source}", "{suffix}"),'
    #         )
    #
    #     lines.extend(
    #         [
    #             ")",
    #             "",
    #         ]
    #     )
    #
    #     return "\n".join(
    #         lines,
    #     )
    
    # # ------------------------------------------------------------------
    #
    # def _load_sites(
    #         self,
    # ) -> list[tuple[str, str, str, str]]:
    #     """
    #     Загрузить список поддерживаемых сайтов.
    #     """
    #
    #     from papershelf.parsers import site_registry_data
    #
    #     importlib.reload(
    #         site_registry_data,
    #     )
    #
    #     return list(
    #         site_registry_data._SITES,
    #     )