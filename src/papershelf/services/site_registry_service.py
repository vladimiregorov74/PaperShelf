from __future__ import annotations

from importlib import reload

from papershelf.models import SupportedSite
from papershelf.parsers import site_registry_data


class SiteRegistryService:
    """
    Работа с реестром поддерживаемых сайтов.
    """

    # ------------------------------------------------------------------

    def get_sites(
        self,
    ) -> list[SupportedSite]:
        """
        Получить список поддерживаемых сайтов.
        """

        reload(site_registry_data)

        sites: list[SupportedSite] = []

        for (
            identifier,
            domain,
            source,
            title_suffix,
        ) in site_registry_data._SITES:

            sites.append(
                SupportedSite(
                    identifier=identifier,
                    domain=domain,
                    source=source,
                    title_suffix=title_suffix,
                )
            )

        return sorted(
            sites,
            key=lambda site: site.source.lower(),
        )
