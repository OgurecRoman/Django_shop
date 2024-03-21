import django.test
import django.urls

import feedback.forms
import feedback.models


class FeedbackFormTests(django.test.TestCase):
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
        text_label = FeedbackFormTests.form.fields["text"].label
        self.assertEqual(text_label, "Текст сообщения")

    def test_text_help(self):
        text_help = FeedbackFormTests.form.fields["text"].help_text
        self.assertEqual(text_help, "Введите текст сообщения")

    def test_mail_label(self):
        text_label = FeedbackFormTests.form.fields["mail"].label
        self.assertEqual(text_label, "Почта пользователя")

    def test_mail_help(self):
        text_help = FeedbackFormTests.form.fields["mail"].help_text
        self.assertEqual(text_help, "Введите свою почту")

    def test_name_label(self):
        text_label = FeedbackFormTests.form.fields["name"].label
        self.assertEqual(text_label, "Имя отправителя")

    def test_name_help(self):
        text_help = FeedbackFormTests.form.fields["name"].help_text
        self.assertEqual(text_help, "Введите имя отправителя")

    def test_create_task(self):
        items_count = feedback.models.Feedback.objects.count()
        form_data = {
            "name": "Абоба",
            "text": "текст",
            "mail": "aboba@mail.com",
        }

        self.assertFalse(
            feedback.models.Feedback.objects.filter(
                text="текст",
            ).exists(),
        )

        self.assertFalse(
            feedback.models.Feedback.objects.filter(
                name="Абоба",
                mail="aboba@mail.com",
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

        self.assertTrue(response.context["form"].has_error("mail"))
        self.assertEqual(
            feedback.models.Feedback.objects.count(),
            items_count,
        )


__all__ = []
