import django.db.models


class FeedbackModel(django.db.models.Model):
    text = django.db.models.TextField(
        "текст", help_text="Введите текст сообщения"
    )

    created_on = django.db.models.DateTimeField(
        "время создания",
        auto_now_add=True,
    )

    mail = django.db.models.EmailField("почта", help_text="Введите свою почту")
