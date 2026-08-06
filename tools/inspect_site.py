from __future__ import annotations

import sys

from site_inspector.inspector import SiteInspector
from site_inspector.report_formatter import ReportFormatter


# ------------------------------------------------------------------


def main() -> None:
    """
    Точка входа.
    """

    if len(sys.argv) != 2:

        print(
            "Использование:\n"
            "python inspect_site.py <url>"
        )

        return

    url = sys.argv[1]

    inspector = SiteInspector()
    inspector.load(
	    url,
    )

    report = inspector.inspect()
    # try:
	#
    #     inspector.load(
    #         url,
    #     )
	#
    #     report = inspector.inspect()
	#
    # except Exception as error:
	#
    #     print(
    #         f"\nОшибка: {error}"
    #     )
	#
    #     return

    print(
        ReportFormatter.format(
            report,
        )
    )


# ------------------------------------------------------------------


if __name__ == "__main__":
    main()