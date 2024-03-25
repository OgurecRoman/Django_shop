import pathlib
import tempfile

import django.conf
import django.test
import django.urls

import feedback.forms
import feedback.models


class FeedbackFormTests(django.test.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.form = feedback.forms.FeedbackForm()
        cls.auther_form = feedback.forms.FeedbackAutherForm()
        cls.files_form = feedback.forms.FeedbackFileForm()

    def test_feedback_correct_context(self):
        response = django.test.Client().get(
            django.urls.reverse("feedback:feedback"),
        )
        self.assertIn("form", response.context)
        self.assertIn("author_form", response.context)
        self.assertIn("files_form", response.context)

    def test_text_label(self):
        text_label = FeedbackFormTests.form.fields["text"].label
        self.assertEqual(text_label, "Текст сообщения")

    def test_text_help(self):
        text_help = FeedbackFormTests.form.fields["text"].help_text
        self.assertEqual(text_help, "Введите текст сообщения")

    def test_mail_label(self):
        text_label = FeedbackFormTests.auther_form.fields["mail"].label
        self.assertEqual(text_label, "Почта пользователя")

    def test_mail_help(self):
        text_help = FeedbackFormTests.auther_form.fields["mail"].help_text
        self.assertEqual(text_help, "Введите свою почту")

    def test_name_label(self):
        text_label = FeedbackFormTests.auther_form.fields["name"].label
        self.assertEqual(text_label, "Имя отправителя")

    def test_name_help(self):
        text_help = FeedbackFormTests.auther_form.fields["name"].help_text
        self.assertEqual(text_help, "Введите имя отправителя")

    def test_unable_create_task(self):
        items_count = feedback.models.Feedback.objects.count()
        form_data = {
            "name": "Абоба",
            "text": "тестовый текст",
            "mail": "notmail",
        }

        response = django.test.Client().post(
            django.urls.reverse("feedback:feedback"),
            data=form_data,
            follow=True,
        )

        self.assertTrue(response.context["author_form"].has_error("mail"))
        self.assertEqual(
            feedback.models.Feedback.objects.count(),
            items_count,
        )

    def test_create_feedback(self):
        items_count = feedback.models.Feedback.objects.count()
        form_data = {
            "name": "Абоба",
            "text": "много абоб",
            "mail": "123@mail.ru",
        }

        self.assertFalse(
            feedback.models.Feedback.objects.filter(
                text="много абоб",
            ).exists(),
        )
        self.assertFalse(
            feedback.models.FeedbackAuther.objects.filter(
                name="Абоба",
                mail="123@mail.ru",
            ).exists(),
        )

        response = django.test.Client().post(
            django.urls.reverse("feedback:feedback"),
            data=form_data,
            follow=True,
        )
        self.assertRedirects(
            response,
            django.urls.reverse("feedback:feedback"),
        )

        self.assertEqual(
            feedback.models.Feedback.objects.count(),
            items_count + 1,
        )

        self.assertTrue(
            feedback.models.Feedback.objects.filter(
                text="много абоб",
            ).exists(),
        )
        self.assertTrue(
            feedback.models.FeedbackAuther.objects.filter(
                name="Абоба",
                mail="123@mail.ru",
            ).exists(),
        )

    @django.test.override_settings(
        MEDIA_ROOT=tempfile.TemporaryDirectory().name,
    )
    def test_file_upload(self):
        files = [
            django.core.files.base.ContentFile(
                f"file_{index}".encode(),
                name="filename",
            )
            for index in range(10)
        ]
        form_data = {
            "name": "Тест",
            "text": "Текст",
            "mail": "123@aboba.ru",
            "file": files,
        }

        django.test.Client().post(
            django.urls.reverse("feedback:feedback"),
            data=form_data,
            follow=True,
        )
        feedback_item = feedback.models.Feedback.objects.get(
            text="Текст",
        )
        self.assertEqual(feedback_item.files.count(), 10)
        feedback_files = feedback_item.files.all()

        media_root = pathlib.Path(django.conf.settings.MEDIA_ROOT)

        for index, file in enumerate(feedback_files):
            uploaded_file = media_root / file.file.path
            self.assertEqual(
                uploaded_file.open().read(),
                f"file_{index}",
            )


__all__ = []
