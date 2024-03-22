from django.contrib import admin

import feedback.models


class FeedbackAuther(admin.TabularInline):
    model = feedback.models.FeedbackAuther
    fields = (
        feedback.models.FeedbackAuther.name.field.name,
        feedback.models.FeedbackAuther.mail.field.name,
    )
    can_delete = False


class FeedbackFile(admin.TabularInline):
    model = feedback.models.FeedbackFile
    fields = (feedback.models.FeedbackFile.file.field.name,)


@admin.register(feedback.models.Feedback)
class FeedBackAdmin(admin.ModelAdmin):
    list_display = (
        feedback.models.Feedback.text.field.name,
        feedback.models.Feedback.status.field.name,
    )

    inlines = (
        FeedbackAuther,
        FeedbackFile,
    )

    def save_model(self, request, obj, form, change):
        status_old = feedback.models.Feedback.objects.get(
            pk=obj.pk,
        ).status
        if status_old != obj.status:
            feedback.models.StatusLog.objects.create(
                user=request.user,
                from_status=status_old,
                to=obj.status,
            )

        super().save_model(request, obj, form, change)


__all__ = []
