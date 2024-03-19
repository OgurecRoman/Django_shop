from django.contrib import admin

import catalog.models

admin.site.register(catalog.models.Category)
admin.site.register(catalog.models.Tag)


class MainImage(admin.TabularInline):
    model = catalog.models.MainImage
    fields = (catalog.models.Image.image.field.name,)


class Image(admin.TabularInline):
    model = catalog.models.Image
    fields = (catalog.models.Image.image.field.name,)


@admin.register(catalog.models.Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = (
        catalog.models.Item.name.field.name,
        catalog.models.Item.is_published.field.name,
        catalog.models.Item.image_tmb,
    )
    readonly_fields = (
        catalog.models.Item.created.field.name,
        catalog.models.Item.updated.field.name,
    )
    list_editable = (catalog.models.Item.is_published.field.name,)
    list_display_links = (catalog.models.Item.name.field.name,)
    filter_horizontal = (catalog.models.Item.tags.field.name,)
    inlines = [
        MainImage,
        Image,
    ]


__all__ = []
