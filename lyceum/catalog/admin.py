from django.contrib import admin

from . import models

admin.site.register(models.Category)
admin.site.register(models.Tag)


@admin.register(models.Item)
class ItemAdmin(admin.ModelAdmin):
    filter_horizontal = (models.Item.tags.field.name,)

    fields = ("is_published", "name", "category", "tags", "text")

    list_display = (
        models.Item.name.field.name,
        models.Item.is_published.field.name,
    )

    list_editable = ("is_published",)
    list_display_links = ("name",)
