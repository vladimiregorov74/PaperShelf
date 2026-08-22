from __future__ import annotations

import importlib
from pathlib import Path

from papershelf.parsers import site_registry_data


class RegistryFileEditor:
    """
    Редактор файла site_registry_data.py.
    """

    # ------------------------------------------------------------------

    def __init__(
        self,
        path: Path,
    ) -> None:

        self._path = path
        
    # ------------------------------------------------------------------
    
    def _load_sites(
            self,
    ) -> list[tuple[str, str, str, str]]:
        """
        Загрузить список поддерживаемых сайтов.
        """
        
        from papershelf.parsers import site_registry_data
        
        importlib.reload(
            site_registry_data,
        )
        
        return list(
            site_registry_data._SITES,
        )
        
    # ------------------------------------------------------------------
    
    def _save_sites(
            self,
            sites: list[tuple[str, str, str, str]],
    ) -> None:
        """
        Записать site_registry_data.py.
        """
        
        text = self._format_registry(
            sites,
        )
        
        self._path.write_text(
            text,
            encoding="utf-8",
        )
        
    # ------------------------------------------------------------------
    
    def _format_registry(
            self,
            sites: list[tuple[str, str, str, str]],
    ) -> str:
        """
        Построить содержимое
        site_registry_data.py.
        """
        
        lines = [
            "from __future__ import annotations",
            "",
            "_SITES: tuple[tuple[str, str, str, str], ...] = (",
            "",
        ]
        
        for identifier, domain, source, suffix in sites:
            lines.append(
                f'    ("{identifier}", "{domain}", "{source}", "{suffix}"),'
            )
        
        lines.extend(
            [
                ")",
                "",
            ]
        )
        
        return "\n".join(
            lines,
        )
        
    # ------------------------------------------------------------------
    
    def remove(
            self,
            identifier: str,
    ) -> None:
        """
        Удалить запись из реестра.
        """
        
        sites = self._load_sites()
        
        sites = [
            site
            for site in sites
            if site[0] != identifier
        ]
        
        self._save_sites(
            sites,
        )