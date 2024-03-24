import http

import django.http
from django.shortcuts import render

import catalog.models
import homepage.forms


def home(request):
    template = "homepage/main.html"
    items = catalog.models.Item.objects.on_main()
    context = {"items": items}
    return render(request, template, context)


def echo(request):
    if request.method != "GET":
        return django.http.HttpResponseNotAllowed(["GET"])

    template = "homepage/echo.html"

    form = homepage.forms.FormEcho()

    context = {
        "form": form,
    }
    return django.shortcuts.render(request, template, context)


def echo_submit(request):
    if request.method != "POST":
        return django.http.HttpResponseNotAllowed(["POST"])

    form = homepage.forms.FormEcho(request.POST or None)
    if form.is_valid():
        return django.http.HttpResponse(form.cleaned_data["text"])

    return django.http.HttpResponseBadRequest("Form is not valid")


def coffee(request):
    if request.user.is_authenticated:
        request.user.profile.coffee_count += 1
        request.user.profile.save()

    return django.http.HttpResponse(
        "Я чайник",
        status=http.HTTPStatus.IM_A_TEAPOT,
    )


__all__ = []
