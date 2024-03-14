import datetime
import random

from django.db.models import Prefetch
from django.http import HttpResponse
import django.shortcuts

import catalog.models


def new(request):
    template = "catalog/special.html"
    items_id = list(
        catalog.models.Item.objects.published()
        .filter(
            created__gte=datetime.date.today() - datetime.timedelta(days=7),
        )
        .values_list("id", flat=True),
    )

    try:
        selected = random.sample(items_id, 5)
    except ValueError:
        selected = items_id

    items = catalog.models.Item.objects.published().filter(pk__in=selected)

    context = {"items": items, "name": "Новинки"}
    return django.shortcuts.render(request, template, context)


def friday(request):
    template = "catalog/special.html"
    items = (
        catalog.models.Item.objects.published()
        .filter(updated__week_day=6)
        .order_by(
            f"-{catalog.models.Item.updated.field.name}",
        )[:5]
    )

    context = {"items": items, "name": "Пятница"}
    return django.shortcuts.render(request, template, context)


def unverified(request):
    template = "catalog/special.html"
    items = (
        catalog.models.Item.objects.on_main()
        .filter(
            created__gte=django.db.models.F(
                catalog.models.Item.updated.field.name,
            )
            - datetime.timedelta(seconds=1),
            created__lte=django.db.models.F(
                catalog.models.Item.updated.field.name,
            )
            + datetime.timedelta(seconds=1),
        )
        .order_by(
            "?",
        )[:5]
    )

    context = {"items": items, "name": "Непроверенное"}
    return django.shortcuts.render(request, template, context)


def item_list(request):
    template = "catalog/item_list.html"
    items = catalog.models.Item.objects.published()
    context = {"items": items}
    return django.shortcuts.render(request, template, context)


def item_detail(request, pk):
    template = "catalog/item.html"
    queryset = catalog.models.Item.objects.published().prefetch_related(
        Prefetch(
            catalog.models.Item.images.field.related_query_name(),
            queryset=catalog.models.Image.objects.only(
                catalog.models.Image.image.field.name,
                catalog.models.Image.item_id.field.name,
            ),
        ),
    )

    item = django.shortcuts.get_object_or_404(queryset, pk=pk)
    context = {"item": item}
    return django.shortcuts.render(request, template, context)


def re_item(request, pk):
    return HttpResponse(pk)


__all__ = []
