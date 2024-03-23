import datetime

from django.conf import settings
from django.contrib import messages
import django.contrib.auth
import django.contrib.auth.decorators
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

import users.forms

__all__ = []


def signup(request):
    form = users.forms.SignUpForm(request.POST or None)
    template = "users/signup.html"
    context = {
        "form": form,
    }
    if request.method == "POST" and form.is_valid():
        user = form.save(commit=False)
        user.is_active = settings.DEFAULT_USER_IS_ACTIVE
        user.save()
        messages.success(request, _("message_signup_success!"))
        return redirect(reverse("users:login"))

    return render(request, template, context)


def activate(request, username):
    user = get_object_or_404(
        django.contrib.auth.get_user_model().objects,
        username=username,
    )
    if timezone.now() > user.date_joined + datetime.timedelta(hours=12):
        messages.success(request, _("message_activate_success!"))
    else:
        messages.error(request, _("message_activate_error!"))

    return redirect(reverse("homepage:main"))


def user_list(request):
    template = "users/user_list.html"

    users = django.contrib.auth.get_user_model().objects.filter(
        is_active=True,
    )
    context = {
        "users": users,
    }
    return render(request, template, context)


def user_detail(request, username):
    template = "users/user_list.html"

    user = get_object_or_404(
        django.contrib.auth.get_user_model().objects,
        username=username,
    )
    context = {
        "user": user,
    }
    return render(request, template, context)
