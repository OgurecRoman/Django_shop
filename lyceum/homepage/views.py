from django.http import HttpResponse


def home(request):
    return HttpResponse("<body>Главная</body>")


def coffee(request):
    return HttpResponse("Я чайник", status=418)
