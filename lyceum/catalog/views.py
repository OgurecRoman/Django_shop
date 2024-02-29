from django.http import HttpResponse
from django.shortcuts import render


def item_list(request):
    template = "catalog/item_list.html"
    context = {}
    return render(request, template, context)


def item_detail(request, pk):
    template = "catalog/item.html"
    context = {"pk": pk}
    return render(request, template, context)


def re_item(request, pk):
    return HttpResponse(pk)


__all__ = []
