from django.urls import path, re_path, register_converter

import catalog.converters
import catalog.views

register_converter(catalog.converters.MyConverter, "mk")

urlpatterns = [
    path("", catalog.views.item_list),
    path("<int:pk>/", catalog.views.item_detail),
    path("converter/<mk:pk>/", catalog.views.re_item),
    re_path(r"re/(?P<pk>[1-9]\d*)/", catalog.views.re_item),
]
