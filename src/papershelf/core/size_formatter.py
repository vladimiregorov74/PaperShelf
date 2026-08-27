from __future__ import annotations


class SizeFormatter:
    """
    Форматирование размеров файлов.
    """

    # ------------------------------------------------------------------

    @staticmethod
    def format(
        size: int,
    ) -> str:
        """
        Представить размер в удобном виде.
        """

        units = (
            "Б",
            "КБ",
            "МБ",
            "ГБ",
            "ТБ",
        )

        value = float(size)

        for unit in units:

            if value < 1024 or unit == units[-1]:

                if unit == "Б":
                    return f"{int(value)} {unit}"

                return f"{value:.1f} {unit}"

            value /= 1024