import django.shortcuts
import django.core.mail

import lyceum.settings
import feedback.forms
import feedback.models


def feedback(request):
    template = "feedback/feedback.html"
    form = feedback.forms.FeedbackForm(request.POST or None)
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
        return django.shortcuts.redirect("catalog:item_list")

    context = {"form": form}
    return django.shortcuts.render(request, template, context)
