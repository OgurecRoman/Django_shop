import time

import django.conf
import django.db.models


class Feedback(django.db.models.Model):
    class Status(django.db.models.TextChoices):
        NEW = "new", "New"
        WORK = "wip", "Work in progress"
        ANSWERED = "ans", "Answered"

    text = django.db.models.TextField(
        "текст",
    )

    created_on = django.db.models.DateTimeField(
        "время создания",
        auto_now_add=True,
    )

    status = django.db.models.CharField(
        "статус",
        max_length=3,
        choices=Status.choices,
        default=Status.NEW,
    )


class FeedbackAuther(django.db.models.Model):
    name = django.db.models.CharField(
        "имя",
        max_length=150,
        null=True,
        blank=True,
    )

    mail = django.db.models.EmailField(
        "почта",
    )

    feedback = django.db.models.OneToOneField(
        Feedback,
        related_name="auther",
        on_delete=django.db.models.CASCADE,
    )


class FeedbackFile(django.db.models.Model):
    def get_path(self, filename):
        return f"uploads/{self.feedback_id}/{time.time()}_{filename}"

    file = django.db.models.FileField(
        "файл",
        upload_to=get_path,
        blank=True,
    )

    feedback = django.db.models.ForeignKey(
        Feedback,
        related_name="files",
        on_delete=django.db.models.CASCADE,
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
        choices=Feedback.Status.choices,
        default=Feedback.Status.NEW,
        db_column="from",
    )

    to = django.db.models.CharField(
        max_length=3,
        choices=Feedback.Status.choices,
        default=Feedback.Status.NEW,
    )


__all__ = []
