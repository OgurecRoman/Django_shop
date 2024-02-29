from django.contrib import admin

import catalog.models

admin.site.register(catalog.models.Category)
admin.site.register(catalog.models.Tag)


class GalleryImageInline(admin.TabularInline):
    model = catalog.models.GalleryImage


class MainImageInline(admin.TabularInline):
    model = catalog.models.MainImage
    can_delete = True


@admin.register(catalog.models.Item)
class ItemAdmin(admin.ModelAdmin):
    inlines = [
        MainImageInline,
        GalleryImageInline,
    ]

    list_display = (
        "get_image",
        catalog.models.Item.name.field.name,
        catalog.models.Item.is_published.field.name,
    )

    list_editable = (catalog.models.Item.is_published.field.name,)
    list_display_links = (catalog.models.Item.name.field.name,)
    filter_horizontal = (catalog.models.Item.tags.field.name,)

    @admin.display(ordering="main_image", description="Главное изображение")
    def get_image(self, obj):
        return obj.main_image.image_thumbnail()


__all__ = [
    GalleryImageInline,
    MainImageInline,
    ItemAdmin,
]
