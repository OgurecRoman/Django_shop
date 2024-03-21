import django.contrib
import django.core.mail
import django.shortcuts
import django.urls

import feedback.forms as feedback_forms
import feedback.models as feedback_models
import lyceum.settings


def feedback(request):
    template = "feedback/feedback.html"
    feedback_form = feedback_forms.FeedbackForm(request.POST or None)
    context = {
        "feedback_form": feedback_form,
    }
    if request.method == "POST" and feedback_form.is_valid():
        name = feedback_form.cleaned_data["name"]
        text = feedback_form.cleaned_data["text"]
        mail_from = lyceum.settings.DJANGO_MAIL
        mail_to = feedback_form.cleaned_data["mail"]

        django.core.mail.send_mail(
            f"Привет, {name}",
            f"{text}",
            mail_from,
            [
                f"{mail_to}",
            ],
            fail_silently=True,
        )
        feedback_item = feedback_models.Feedback.objects.create(
            **feedback_form.cleaned_data,
        )
        feedback_item.save()

        django.contrib.messages.success(
            request,
            "Форма успешно отправлена!",
        )

        return django.shortcuts.redirect(
            django.urls.reverse("feedback:feedback"),
        )

    return django.shortcuts.render(request, template, context)


__all__ = []
