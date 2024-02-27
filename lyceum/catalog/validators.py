import re

import django.core.exceptions

# import django.utils.deconstruct

WORDS_REGEX = re.compile(r"\w+|\W+")


def validate_brilliant(value):
    words = set(WORDS_REGEX.findall(value.lower()))
    if not {"превосходно", "роскошно"} & words:
        raise django.core.exceptions.ValidationError(
            "Не найдено слов 'превосходно' или 'роскошно'"
        )


#
# @django.utils.deconstruct.deconstructible
# class WordsValidator:
#     def __init__(self, *args):
#         self.validate_words = {word.lower() for word in args}
#         self.joined_words = ", ".join(self.validate_words)
#
#     def __call__(self, value):
#         words = set(WORDS_REGEX.findall(value.lower()))
#         if not self.validate_words & words:
#             raise django.core.exceptions.ValidationError(
#                 f"В тексте {value} нет слов: {self.joined_words}"
#             )
