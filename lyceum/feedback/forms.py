import django.forms

import feedback.models


class FeedbackForm(django.forms.ModelForm):
    class Meta:
        model = feedback.models.FeedbackModel
        fields = (
            feedback.models.FeedbackModel.text.field.name,
            feedback.models.FeedbackModel.mail.field.name,
        )
        labels = {
            feedback.models.FeedbackModel.text.field.name:
                "Текст сообщения",
            feedback.models.FeedbackModel.mail.field.name:
                "Почта пользователя",
        }


__all__ = []
