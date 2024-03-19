import django.forms

from feedback.models import FeedbackModel


class FeedbackForm(django.forms.ModelForm):
    class Meta:
        model = FeedbackModel
        fields = (
            FeedbackModel.text.field.name,
            FeedbackModel.mail.field.name,
        )
        labels = {
            FeedbackModel.text.field.name: "Текст сообщения",
            FeedbackModel.mail.field.name: "Почта пользователя",
        }

        help_texts = {
            FeedbackModel.text.field.name: "Введите текст сообщения",
            FeedbackModel.mail.field.name: "Введите свою почту",
        }


__all__ = []
