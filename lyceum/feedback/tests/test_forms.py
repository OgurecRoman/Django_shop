import django.test
import django.urls

import feedback.forms
import feedback.models


class FormTests(django.test.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.form = feedback.forms.FeedbackForm()

    def test_feedback_correct_context(self):
        response = django.test.Client().get(
            django.urls.reverse("feedback:feedback"),
        )
        self.assertIn("form", response.context)

    def test_text_label(self):
        text_label = FormTests.form.fields["text"].label
        self.assertEqual(text_label, "Текст сообщения")

    def test_text_help(self):
        text_help = FormTests.form.fields["text"].help_text
        self.assertEqual(text_help, "Введите текст сообщения")

    def test_mail_label(self):
        text_label = FormTests.form.fields["mail"].label
        self.assertEqual(text_label, "Почта пользователя")

    def test_mail_help(self):
        text_help = FormTests.form.fields["mail"].help_text
        self.assertEqual(text_help, "Введите свою почту")

    def test_create_task(self):
        items_count = feedback.models.FeedbackModel.objects.count()
        form_data = {
            "text": "тестовый текст",
            "mail": "1@mail.ru",
        }

        self.assertFalse(
            feedback.models.FeedbackModel.objects.filter(
                text="тестовый текст",
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
            feedback.models.FeedbackModel.objects.count(),
            items_count + 1,
        )

    def test_unable_create_task(self):
        items_count = feedback.models.FeedbackModel.objects.count()
        form_data = {
            "text": "тестовый текст",
            "mail": "notmail",
        }

        response = django.test.Client().post(
            django.urls.reverse("feedback:feedback"),
            data=form_data,
            follow=True,
        )

        self.assertTrue(response.context["form"].has_error("mail"))
        self.assertEqual(
            feedback.models.FeedbackModel.objects.count(),
            items_count,
        )


__all__ = []
