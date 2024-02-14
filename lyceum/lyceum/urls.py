from django.conf import settings
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("homepage.urls")),
    path("catalog/", include("catalog.urls")),
    path("about/", include("about.urls")),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    import debug_toolbar

    # добавляем к списку адресов список адресов из debug_toolbar
    urlpatterns += (path("__debug__/", include(debug_toolbar.urls)),)
