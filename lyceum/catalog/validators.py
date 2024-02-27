import re

import django.core.exceptions

WORDS_REGEX = re.compile(r"\w+|\W+")


def validate_brilliant(value):
    words = set(WORDS_REGEX.findall(value.lower()))
    if not {"превосходно", "роскошно"} & words:
        raise django.core.exceptions.ValidationError(
            "Не найдено слов 'превосходно' или 'роскошно'",
        )
