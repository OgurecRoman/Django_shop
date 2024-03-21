import django.contrib
import django.core.mail
import django.shortcuts
import django.urls

import feedback.forms as feedback_forms
import lyceum.settings


def feedback(request):
    template = "feedback/feedback.html"
    feedback_form = feedback_forms.FeedbackForm(request.POST or None)
    context = {
        "form": feedback_form,
    }
    if request.method == "POST" and feedback_form.is_valid():
        name = feedback_form.cleaned_data["name"]
        if name is None:
            name = ""

        text = feedback_form.cleaned_data["text"]
        mail_from = lyceum.settings.DJANGO_MAIL
        mail_to = feedback_form.cleaned_data["mail"]

        django.core.mail.send_mail(
            "Фидбек",
            f"Привет {name}\n{text}",
            mail_from,
            [
                f"{mail_to}",
            ],
            fail_silently=True,
        )

        feedback_form.save()

        django.contrib.messages.success(
            request,
            "Форма успешно отправлена!",
        )

        return django.shortcuts.redirect(
            django.urls.reverse("feedback:feedback"),
        )

    return django.shortcuts.render(request, template, context)


__all__ = []
