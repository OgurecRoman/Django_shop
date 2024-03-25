import datetime

from django.conf import settings
from django.contrib import messages
import django.contrib.auth
import django.contrib.auth.decorators
import django.core.mail
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

import users.forms
import users.models

__all__ = []


def signup(request):
    form = users.forms.CustomUserCreationForm(request.POST or None)
    template = "users/signup.html"
    context = {
        "form": form,
    }
    if request.method == "POST" and form.is_valid():
        user = form.save(commit=False)
        user.is_active = settings.DEFAULT_USER_IS_ACTIVE
        user.save()
        profile = users.models.Profile.objects.create(user=user)
        profile.save()

        activate_url = django.urls.reverse(
            "users:activate",
            kwargs={"pk": user.id},
        )
        django.core.mail.send_mail(
            "",
            f"Приветб {user.username}\n"
            f"Для активации аккаунта перейдите по ссылке f'{activate_url}'",
            django.conf.settings.DJANGO_MAIL,
            [user.email],
            fail_silently=False,
        )
        return redirect(reverse("homepage:main"))

    return render(request, template, context)


def activate(request, pk):
    user = get_object_or_404(
        django.contrib.auth.get_user_model().objects,
        pk=pk,
    )
    if timezone.now() > user.date_joined + datetime.timedelta(hours=12):
        messages.success(request, _("message_activate_success!"))
    else:
        messages.error(request, _("message_activate_error!"))

    return redirect(reverse("homepage:main"))


def user_list(request):
    template = "users/user_list.html"

    active_users = users.models.User.objects.active()
    context = {
        "users": active_users,
    }
    return render(request, template, context)


def user_detail(request, pk: int):
    template = "users/user_detail.html"

    user = get_object_or_404(
        users.models.User.objects.active(),
        pk=pk,
    )
    context = {
        "user": user,
    }
    return render(request, template, context)


@django.contrib.auth.decorators.login_required
def profile(request):
    template = "users/profile.html"
    user_form = users.forms.CustomUserChangeForm(
        request.POST or None,
        instance=request.user,
    )
    profile_form = users.forms.ProfileForm(
        request.POST or None,
        request.FILES or None,
        instance=request.user.profile,
    )
    context = {
        "user": request.user,
        "form": user_form,
        "profile_form": profile_form,
    }
    if (
        request.method == "POST"
        and user_form.is_valid()
        and profile_form.is_valid()
    ):
        user_form.save()
        profile_form.save()
        django.contrib.messages.success(request, "Изменения сохранены")
        return redirect(django.urls.reverse("users:profile"))

    return render(request, template, context)
