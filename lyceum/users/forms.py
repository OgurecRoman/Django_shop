import django.contrib.auth.forms
from django.forms import ModelForm

import users.models


class BootstrapForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"


class CustomUserCreationForm(
    BootstrapForm,
    django.contrib.auth.forms.UserCreationForm,
):
    class Meta(django.contrib.auth.forms.UserCreationForm.Meta):
        model = users.models.User
        fields = (
            users.models.User.username.field.name,
            users.models.User.email.field.name,
        )


class CustomUserChangeForm(
    BootstrapForm,
    django.contrib.auth.forms.UserChangeForm,
):
    password = None

    class Meta(django.contrib.auth.forms.UserChangeForm.Meta):
        fields = (
            users.models.User.first_name.field.name,
            users.models.User.last_name.field.name,
        )


class ProfileForm(BootstrapForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        coffee = users.models.Profile.coffee_count.field.name
        self.fields[coffee].disabled = True

    class Meta:
        model = users.models.Profile
        fields = [
            model.birthday.field.name,
            model.image.field.name,
            model.coffee_count.field.name,
        ]


__all__ = []
