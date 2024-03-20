import django.forms


class FormEcho(django.forms.Form):
    text = django.forms.CharField(
        widget=django.forms.Textarea,
        label="Текст",
        help_text="Введите текст",
    )


__all__ = []
