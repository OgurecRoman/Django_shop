from django.urls import path

import homepage.views

app_name = "homepage"

urlpatterns = [
    path("", homepage.views.home),
    path("main/", homepage.views.main, name="main"),
    path("coffee/", homepage.views.coffee),
]
