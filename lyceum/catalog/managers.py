import datetime

import django.core.validators
import django.db.models
import django.utils.safestring

import catalog.models
import catalog.validators


class Itemmanager(django.db.models.Manager):
    def published(self):
        tags_pref = django.db.models.Prefetch(
            catalog.models.Item.tags.field.name,
            queryset=catalog.models.Tag.objects.filter(
                is_published=True,
            ).only(
                catalog.models.Tag.name.field.name,
            ),
        )

        queryset = self.get_queryset().filter(
            is_published=True,
            category__is_published=True,
        )

        select = queryset.select_related(
            catalog.models.Item.category.field.name,
            catalog.models.Item.main_image.related.name,
        )

        prefetch = select.prefetch_related(
            tags_pref,
        )

        name = catalog.models.Item.name.field.name
        text = catalog.models.Item.text.field.name
        image = catalog.models.Item.main_image.related.name
        category = catalog.models.Item.category.field.name
        tags = catalog.models.Item.tags.field.name
        category_name = catalog.models.Category.name.field.name
        tag_name = catalog.models.Tag.name.field.name

        only_list = [
            name,
            text,
            image,
            f"{category}__{category_name}",
            f"{tags}__{tag_name}",
        ]

        return prefetch.only(*only_list)

    def on_main(self):
        return (
            self.published()
            .filter(
                is_on_main=True,
            )
            .order_by(
                catalog.models.Item.name.field.name,
            )
        )

    def date(self):
        return self.on_main().filter(
            created__gte=django.db.models.F(
                catalog.models.Item.updated.field.name,
            )
                         - datetime.timedelta(seconds=1),
            created__lte=django.db.models.F(
                catalog.models.Item.updated.field.name,
            )
                         + datetime.timedelta(seconds=1),
        )

    def pref_image(self):
        return self.published().prefetch_related(
            django.db.models.Prefetch(
                catalog.models.Item.images.field.related_query_name(),
                queryset=catalog.models.Image.objects.only(
                    catalog.models.Image.image.field.name,
                    catalog.models.Image.item_id.field.name,
                ),
            ),
        )

    def news(self):
        return self.published().filter(
            created__gte=datetime.date.today() - datetime.timedelta(days=7),
        ).values_list("id", flat=True),


__all__ = []
