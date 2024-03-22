import django.forms

from feedback.models import Feedback, FeedbackAuther, FeedbackFile


class BootstrapForm(django.forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"


class FeedbackAutherForm(BootstrapForm):
    class Meta:
        model = FeedbackAuther
        fields = (
            FeedbackAuther.name.field.name,
            FeedbackAuther.mail.field.name,
        )
        labels = {
            FeedbackAuther.name.field.name: "Имя отправителя",
            FeedbackAuther.mail.field.name: "Почта пользователя",
        }

        help_texts = {
            FeedbackAuther.name.field.name: "Введите имя отправителя",
            FeedbackAuther.mail.field.name: "Введите свою почту",
        }


class FeedbackFileForm(BootstrapForm):
    class Meta:
        model = FeedbackFile
        fields = (FeedbackFile.file.field.name,)
        help_texts = {
            FeedbackFile.file.field.name: "Приложите файлы",
        }
        widgets = {
            FeedbackFile.file.field.name: (
                django.forms.FileInput(
                    attrs={
                        "class": "form-control",
                        "type": "file",
                        "multiple": True,
                    },
                )
            ),
        }


class FeedbackForm(BootstrapForm):
    class Meta:
        model = Feedback
        fields = (Feedback.text.field.name,)
        exclude = (Feedback.created_on.field.name,)
        labels = {
            Feedback.text.field.name: "Текст сообщения",
        }

        help_texts = {
            Feedback.text.field.name: "Введите текст сообщения",
        }


__all__ = []
