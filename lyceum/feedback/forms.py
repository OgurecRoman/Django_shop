import django.forms

from feedback.models import FeedbackModel


class BootstrapForm(django.forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"


class FeedbackForm(BootstrapForm):
    class Meta:
        model = FeedbackModel
        fields = (
            FeedbackModel.name.field.name,
            FeedbackModel.text.field.name,
            FeedbackModel.mail.field.name,
        )
        exclude = (FeedbackModel.created_on,)
        labels = {
            FeedbackModel.name.field.name: "Имя отправителя",
            FeedbackModel.text.field.name: "Текст сообщения",
            FeedbackModel.mail.field.name: "Почта пользователя",
        }

        help_texts = {
            FeedbackModel.name.field.name: "Введите имя отправителя",
            FeedbackModel.text.field.name: "Введите текст сообщения",
            FeedbackModel.mail.field.name: "Введите свою почту",
        }


__all__ = []
