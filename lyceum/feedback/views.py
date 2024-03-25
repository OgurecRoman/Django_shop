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
    author_form = feedback_forms.FeedbackAutherForm(request.POST or None)
    files_form = feedback_forms.FeedbackFileForm(request.POST or None)

    context = {
        "feedback_form": feedback_form,
        "author_form": author_form,
        "files_form": files_form,
    }

    forms = (feedback_form, author_form, files_form)

    if request.method == "POST" and all(form.is_valid() for form in forms):
        name = author_form.cleaned_data["name"]
        if name is None:
            name = ""

        text = feedback_form.cleaned_data["text"]
        mail_from = lyceum.settings.DJANGO_MAIL
        mail_to = author_form.cleaned_data["mail"]

        django.core.mail.send_mail(
            "Фидбек",
            f"Привет {name}\n{text}",
            mail_from,
            [
                f"{mail_to}",
            ],
            fail_silently=True,
        )

        feedback_item = feedback_form.save()

        feedback_models.FeedbackAuther.objects.create(
            feedback=feedback_item,
            **author_form.cleaned_data,
        )

        for file in request.FILES.getlist(
            feedback_models.FeedbackFile.file.field.name,
        ):
            feedback_models.FeedbackFile.objects.create(
                feedback=feedback_item,
                file=file,
            )

        django.contrib.messages.success(
            request,
            "Форма успешно отправлена!",
        )

        return django.shortcuts.redirect(
            django.urls.reverse("feedback:feedback"),
        )

    return django.shortcuts.render(request, template, context)


__all__ = []
