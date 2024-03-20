import django.conf
import django.db.models


class FeedbackModel(django.db.models.Model):
    class Status(django.db.models.TextChoices):
        NEW = "new", "New"
        WORK = "job", "Work"
        ANSWERED = "ans", "Answered"

    name = django.db.models.CharField(
        "имя",
        max_length=100,
    )
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

    status = django.db.models.CharField(
        "статус",
        max_length=3,
        choices=Status.choices,
        default=Status.NEW,
    )


class StatusLog(django.db.models.Model):
    user = django.db.models.ForeignKey(
        django.conf.settings.AUTH_USER_MODEL,
        on_delete=django.db.models.CASCADE,
        verbose_name="пользователь",
    )

    timestamp = django.db.models.DateTimeField(
        "время создания",
        auto_now_add=True,
    )

    from_status = django.db.models.CharField(
        max_length=3,
        choices=FeedbackModel.Status.choices,
        default=FeedbackModel.Status.NEW,
        db_column="from",
    )

    to = django.db.models.CharField(
        max_length=3,
        choices=FeedbackModel.Status.choices,
        default=FeedbackModel.Status.NEW,
    )


__all__ = []
