import django.forms


class FormEcho(django.forms.Form):
    text = django.forms.CharField(
        widget=django.forms.Textarea,
    )


__all__ = []
