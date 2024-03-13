import http

from django.db.models import Prefetch
from django.http import HttpResponse
from django.shortcuts import render

import catalog.models


def home(request):
    template = "homepage/main.html"
    items = (
        catalog.models.Item.objects.filter(
            is_published=True,
            category__is_published=True,
            is_on_main=True,
        )
        .select_related(
            "category",
            "main_image",
        )
        .prefetch_related(
            Prefetch(
                "tags",
                queryset=catalog.models.Tag.objects.filter(
                    is_published=True,
                ).only("name"),
            ),
        )
        .only(
            "name",
            "text",
            "id",
            "category",
            "tags",
        )
        .order_by("name")
    )
    context = {"items": items}
    return render(request, template, context)


def coffee(request):
    return HttpResponse("Я чайник", status=http.HTTPStatus.IM_A_TEAPOT)


__all__ = []
