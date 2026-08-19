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
    

    ("DAN_IT", "dan-it.com.ua", "Dan It", ""),
    ("WEZOM", "wezom.academy", "Wezom", ""),
    ("METANIT", "metanit.com", "Metanit", ""),
    ("GITHUB", "github.com", "Github", ""),
    ("PRODUCTSTAR", "productstar.ru", "Productstar", ""),
    ("HABR", "habr.com", "Habr", ""),
)
