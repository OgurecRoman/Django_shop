from django.http import HttpResponse


def item_list(request):
    return HttpResponse("<body>Список элементов</body>")


def item_detail(request, pk):
    return HttpResponse("<body>Подробно элемент</body>")


def re_item(request, pk):
    return HttpResponse(pk)


def conv_item(request, ind):
    return HttpResponse(ind)
