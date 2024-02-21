from django.urls import path, re_path, register_converter

from . import converters, views

register_converter(converters.MyConverter, "mk")

urlpatterns = [
    path("", views.item_list),
    path("<int:pk>/", views.item_detail),
    path("converter/<mk:pk>/", views.re_item),
    re_path(r"re/(?P<pk>[1-9]\d*)/", views.re_item),
]
