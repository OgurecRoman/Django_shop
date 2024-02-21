import http

from django.http import HttpResponse


def home(request):
    return HttpResponse("Главная")


def coffee(request):
    return HttpResponse("Я чайник", status=http.HTTPStatus.IM_A_TEAPOT)
