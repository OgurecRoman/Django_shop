import datetime
import random

import django.shortcuts

from catalog.models import Category, Item


def new(request):
    template = "catalog/special.html"
    items_id = list(Item.objects.news())

    try:
        selected = random.sample(items_id, 5)
    except ValueError:
        selected = items_id

    items = Item.objects.published().order_by(
        f"{Item.category.field.name}__{Category.name.field.name}",
        Item.name.field.name,
    )
    items = items.filter(pk__in=selected)
    context = {"items": items, "name": "Новинки"}
    return django.shortcuts.render(request, template, context)


def friday(request):
    template = "catalog/special.html"
    items = Item.objects.published().filter(updated__week_day=6)
    items = items.order_by(
        f"-{Item.updated.field.name}",
    )

    context = {"items": items[:5], "name": "Пятница"}
    return django.shortcuts.render(request, template, context)


def unverified(request):
    template = "catalog/special.html"
    items = Item.objects.date().order_by(
        "?",
    )[:5]

    context = {"items": items, "name": "Непроверенное"}
    return django.shortcuts.render(request, template, context)


def item_list(request):
    template = "catalog/item_list.html"
    items = Item.objects.published()
    context = {"items": items}
    return django.shortcuts.render(request, template, context)


def item_detail(request, pk):
    template = "catalog/item.html"
    queryset = Item.objects.published()

    item = django.shortcuts.get_object_or_404(queryset, pk=pk)
    context = {"item": item}
    return django.shortcuts.render(request, template, context)


__all__ = []
