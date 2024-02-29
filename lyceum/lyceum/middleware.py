import re

from django.conf import settings

WORDS_REG = re.compile(r"\w+|\W+")
NOT_RUSSIAN_REG = re.compile(r"^[^а-яА-ЯёЁ\s]+$")


class ReverseMiddleware:
    count = 0

    def __init__(self, get_response):
        self.get_response = get_response

    @classmethod
    def check_need_reverse(cls):
        if not settings.ALLOW_REVERSE:
            return False

        cls.count += 1
        if cls.count != 10:
            return False
        cls.count = 0
        return True

    def __call__(self, request):
        if not self.check_need_reverse():
            return self.get_response(request)

        response = self.get_response(request)
        content = response.content.decode()
        words = WORDS_REG.findall(content)

        transformed = [
            word if NOT_RUSSIAN_REG.search(word) else word[::-1]
            for word in words
        ]

        response.content = "".join(transformed).encode()
        return response


__all__ = []
