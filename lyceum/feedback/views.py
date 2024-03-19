import django.core.mail
import django.shortcuts

import feedback.forms as feedback_forms
import lyceum.settings


def feedback(request, text=""):
    template = "feedback/feedback.html"
    form = feedback_forms.FeedbackForm(request.POST or None)
    if form.is_valid():
        text = form.cleaned_data.get("text")
        mail_from = lyceum.settings.DJANGO_MAIL
        mail_to = form.cleaned_data.get("mail")
        django.core.mail.send_mail(
            "Заголовок",
            text,
            mail_from,
            [
                mail_to,
            ],
            fail_silently=False,
        )
        return django.shortcuts.redirect(
            "feedback:feedback",
            text="Форма успешно отправлена!",
        )

    context = {
        "form": form,
        "text": text,
    }
    return django.shortcuts.render(request, template, context)


__all__ = []
