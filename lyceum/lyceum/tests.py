import re

from django.test import Client, override_settings, TestCase

import parameterized

WORDS_REG = re.compile(r"\w+|\W+")
RUSSIAN_REG = re.compile(r"^[а-яА-ЯёЁ\s]+$")


def middleware(line):
    words = WORDS_REG.findall(line)

    transformed = [
        word[::-1] if RUSSIAN_REG.search(word) else word for word in words
    ]

    return "".join(transformed)


class MiddlewareTests(TestCase):
    @parameterized.parameterized.expand(
        [
            ("Я чайник", "Я кинйач"),
            ("Тестирование с латиabcницей", "еинаворитсеТ с латиabcницей"),
            ("Тестирование слипшихсяслов", "еинаворитсеТ волсясхишпилс"),
            ("Тестирование знак!!!!ов", "еинаворитсеТ канз!!!!во"),
            ("Тестирование <tags>", "еинаворитсеТ <tags>"),
        ],
    )
    def test_reverse_true(self, line, reverse_line):
        self.assertEqual(middleware(line), reverse_line)


class CatalogStaticURLTests(TestCase):
    @override_settings(ALLOW_REVERSE=True)
    def test_catalog_endpoint_true(self):
        contents = []
        for _ in range(10):
            response = Client().get("/coffee/")
            contents.append(response.content.decode("utf-8"))

        self.assertIn("Я чайник", contents)
        self.assertEqual(contents.count("Я кинйач"), 1)

    @override_settings(ALLOW_REVERSE=False)
    def test_catalog_endpoint_const_false(self):
        contents = []
        for _ in range(10):
            response = Client().get("/coffee/")
            contents.append(response.content.decode("utf-8"))

        self.assertIn("Я чайник", contents)
        self.assertNotIn("Я кинйач", contents)


__all__ = []
