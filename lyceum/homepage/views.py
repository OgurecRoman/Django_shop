import http

from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    template = "homepage/main.html"
    context = {}
    return render(request, template, context)


def coffee(request):
    return HttpResponse("Я чайник", status=http.HTTPStatus.IM_A_TEAPOT)


__all__ = [
    home,
    coffee,
]
