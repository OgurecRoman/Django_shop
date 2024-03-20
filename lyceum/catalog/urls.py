from django.urls import path

import catalog.views

app_name = "catalog"

urlpatterns = [
    path("", catalog.views.item_list, name="item_list"),
    path("<int:pk>/", catalog.views.item_detail, name="item"),
    path("new/", catalog.views.new, name="new"),
    path("unverified/", catalog.views.unverified, name="unverified"),
    path("friday/", catalog.views.friday, name="friday"),
]
