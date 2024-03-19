import django.db.models


class FeedbackModel(django.db.models.Model):
    text = django.db.models.TextField(
        "текст",
    )

    created_on = django.db.models.DateTimeField(
        "время создания",
        auto_now_add=True,
    )

    mail = django.db.models.EmailField(
        "почта",
    )


__all__ = []
