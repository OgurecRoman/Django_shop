from django.urls import path, re_path, register_converter

from . import converters, views

register_converter(converters.MyConverter, "mk")

urlpatterns = [
    path("catalog/", views.item_list),
    path("catalog/<int:pk>/", views.item_detail),
    re_path(r"catalog/re/(?P<pk>[1-9]\d*)$", views.re_item),
    path("catalog/converter/<mk:ind>/", views.conv_item),
]
