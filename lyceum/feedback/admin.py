from django.contrib import admin

import feedback.models


@admin.register(feedback.models.FeedbackModel)
class FeedBackAdmin(admin.ModelAdmin):
    list_display = (
        feedback.models.FeedbackModel.name.field.name,
        feedback.models.FeedbackModel.text.field.name,
        feedback.models.FeedbackModel.mail.field.name,
        feedback.models.FeedbackModel.status.field.name,
    )

    def save_model(self, request, obj, form, change):
        status_old = feedback.models.FeedbackModel.objects.get(
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
