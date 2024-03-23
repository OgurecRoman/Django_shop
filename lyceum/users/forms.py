from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, NumberInput

import users.models


class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta(UserCreationForm.Meta):
        fields = (
            "username",
            "email",
        )


class ProfileForm(ModelForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta(UserCreationForm.Meta):
        model = users.models.Profile
        fields = [
            model.birthday.field.name,
            model.image.field.name,
            model.coffee_count.field.name,
        ]

        widgets = {
            users.models.Profile.coffee_count.field.name: NumberInput(
                attrs={"readonly": "readonly"},
            ),
        }


__all__ = []
