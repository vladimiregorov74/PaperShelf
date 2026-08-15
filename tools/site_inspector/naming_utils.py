from __future__ import annotations

import re

# ------------------------------------------------------------------


def domain_prefix(
    domain: str,
) -> str:
    """
    Преобразовать доменное имя в префикс констант/идентификатор.

    Например:

    metanit.com -> METANIT
    habr.com -> HABR
    dan-it.com.ua -> DAN_IT

    Любые символы, недопустимые в имени Python-переменной (дефис,
    двоеточие порта и т.п.), заменяются на "_", иначе сгенерированный
    файл не импортируется (SyntaxError).
    """

    name = domain.split(
        ".",
        1,
    )[0]

    name = re.sub(
        r"[^0-9a-zA-Z_]",
        "_",
        name,
    )

    if name and name[0].isdigit():
        name = f"_{name}"

    return name.upper()


def guess_source_name(
    domain: str,
) -> str:
    """
    Угадать отображаемое имя источника по домену.

    Например:

    metanit.com -> Metanit
    dan-it.com.ua -> Dan It
    habr.com -> Habr

    Это только дефолт "на глаз" (капитализация частей до первой
    точки) — детектор не может достоверно угадать желаемое
    брендированное имя (например "DAN IT Education" вместо
    "Dan It"), при необходимости переопределяется флагом --source
    в inspect_site.py.
    """

    name = domain.split(
        ".",
        1,
    )[0]

    parts = re.split(
        r"[-_]+",
        name,
    )

    return " ".join(
        part.capitalize()
        for part in parts
        if part
    )
