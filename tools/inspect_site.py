from __future__ import annotations

import argparse

from site_inspector.inspector import SiteInspector
from site_inspector.report_formatter import ReportFormatter


# ------------------------------------------------------------------


def main() -> None:
    """
    Точка входа.
    """

    parser = argparse.ArgumentParser(
        description=(
            "Анализ страницы: поиск контейнера статьи, автора, "
            "мусора для очистки. Обновляет selectors.py и "
            "site_registry.py в src/papershelf/parsers."
        ),
    )

    parser.add_argument(
        "url",
        help="Адрес страницы для анализа.",
    )

    parser.add_argument(
        "--source",
        default=None,
        help=(
            "Отображаемое имя источника для site_registry.py "
            '(например "DAN IT Education"). Если не указано — '
            "подбирается автоматически по домену "
            '(dan-it.com.ua -> "Dan It"). Детектор не может '
            "достоверно угадать желаемый брендинг, поэтому при "
            "необходимости укажите явно."
        ),
    )

    parser.add_argument(
        "--title-suffix",
        default="",
        help=(
            "Суффикс, отрезаемый от <title> страницы "
            '(например " / Хабр"). Детектор не может определить '
            "его сам — это вопрос брендинга конкретного сайта, "
            "не структуры DOM. По умолчанию не отрезается."
        ),
    )

    args = parser.parse_args()

    inspector = SiteInspector()

    inspector.load(
        args.url,
    )
    
    report = inspector.inspect(
        source=args.source,
        title_suffix=args.title_suffix,
    )

    print(
        ReportFormatter.format(
            report,
        )
    )


# ------------------------------------------------------------------


if __name__ == "__main__":
    main()
