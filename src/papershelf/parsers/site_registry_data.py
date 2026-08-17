"""
Данные реестра сайтов — ЧИСТЫЕ данные, без кода.

НЕ РЕДАКТИРУЙТЕ ВРУЧНУЮ — перезаписывается целиком при
каждом запуске tools/inspect_site.py <url> (по префиксу
сайта, остальные строки не трогаются). Логика сборки
SiteConfig из этих данных — в site_registry.py, который
инструмент никогда не переписывает.
"""

from __future__ import annotations

_SITES: tuple[tuple[str, str, str, str], ...] = (
    
    ("HABR", "habr.com", "Habr", " / Хабр"),
    ("DAN_IT", "dan-it.com.ua", "DAN IT Education", ""),
    ("WEZOM", "wezom.academy", "Wezom", ""),
    ("PRODUCTSTAR", "productstar.ru", "Productstar", ""),
    ("METANIT", "metanit.com", "Metanit", ""),
)
