from django.urls import path, re_path, register_converter

import catalog.converters
import catalog.views

app_name = "catalog"

register_converter(catalog.converters.MyConverter, "mk")

urlpatterns = [
    path("", catalog.views.item_list, name="item_list"),
    path("<int:pk>/", catalog.views.item_detail, name="item"),
    path("converter/<mk:pk>/", catalog.views.item_detail),
    path("new/", catalog.views.new, name="new"),
    path("unverified/", catalog.views.unverified, name="unverified"),
    path("friday/", catalog.views.friday, name="friday"),
    re_path(r"re/(?P<pk>[1-9]\d*)/", catalog.views.item_detail),
]
