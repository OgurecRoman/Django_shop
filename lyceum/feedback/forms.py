import django.forms

from feedback.models import Feedback


class BootstrapForm(django.forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"


class FeedbackForm(BootstrapForm):
    class Meta:
        model = Feedback
        fields = (
            Feedback.name.field.name,
            Feedback.text.field.name,
            Feedback.mail.field.name,
            Feedback.status.field.name,
        )
        exclude = (Feedback.created_on,)
        labels = {
            Feedback.name.field.name: "Имя отправителя",
            Feedback.text.field.name: "Текст сообщения",
            Feedback.mail.field.name: "Почта пользователя",
            Feedback.status.field.name: "Статус",
        }

        help_texts = {
            Feedback.name.field.name: "Введите имя отправителя",
            Feedback.text.field.name: "Введите текст сообщения",
            Feedback.mail.field.name: "Введите свою почту",
            Feedback.status.field.name: "Установите статус",
        }


__all__ = []
