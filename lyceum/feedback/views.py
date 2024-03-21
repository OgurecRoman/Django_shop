import django.contrib
import django.core.mail
import django.shortcuts

import feedback.forms as feedback_forms
import feedback.models as feedback_models
import lyceum.settings


def feedback(request):
    template = "feedback/feedback.html"
    form = feedback_forms.FeedbackForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        name = form.cleaned_data["name"]
        text = form.cleaned_data["text"]
        mail_from = lyceum.settings.DJANGO_MAIL
        mail_to = form.cleaned_data["mail"]
        django.core.mail.send_mail(
            "Заголовок",
            f"Привет, {name}\n{text}",
            mail_from,
            [
                f"{mail_to}",
            ],
            fail_silently=True,
        )
        feedback_item = feedback_models.Feedback.objects.create(
            **form.cleaned_data,
        )
        feedback_item.save()

        django.contrib.messages.success(
            request,
            "Форма успешно отправлена!",
        )

        return django.shortcuts.redirect(
            "feedback:feedback",
        )

    context = {
        "form": form,
    }
    return django.shortcuts.render(request, template, context)


__all__ = []
