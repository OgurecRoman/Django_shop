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
        )
        exclude = (Feedback.created_on.field.name,)
        labels = {
            Feedback.name.field.name: "Имя отправителя",
            Feedback.text.field.name: "Текст сообщения",
            Feedback.mail.field.name: "Почта пользователя",
        }

        help_texts = {
            Feedback.name.field.name: "Введите имя отправителя",
            Feedback.text.field.name: "Введите текст сообщения",
            Feedback.mail.field.name: "Введите свою почту",
        }


__all__ = []
