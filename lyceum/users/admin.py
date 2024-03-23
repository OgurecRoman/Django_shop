from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

import users.models


class ProfileInlined(admin.TabularInline):
    model = users.models.Profile
    fields = [
        users.models.Profile.birthday.field.name,
        users.models.Profile.image.field.name,
        users.models.Profile.coffee_count.field.name,
    ]
    readonly_fields = (users.models.Profile.coffee_count.field.name,)
    can_delete = False


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInlined,)


admin.site.unregister(User)
admin.site.register(
    User,
    UserAdmin,
)

__all__ = []
