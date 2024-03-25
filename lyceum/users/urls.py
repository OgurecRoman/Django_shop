from typing import Any

import django.contrib.auth.forms
import django.contrib.auth.views
from django.urls import path, reverse_lazy

import users.views


class CustomAuthenticationForm(django.contrib.auth.forms.AuthenticationForm):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"


class CustomPasswordChangeForm(django.contrib.auth.forms.PasswordChangeForm):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"


class CustomPasswordResetForm(django.contrib.auth.forms.PasswordResetForm):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"


class CustomPasswordSetForm(django.contrib.auth.forms.SetPasswordForm):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"


app_name = "users"

login = django.contrib.auth.views.LoginView.as_view(
    template_name="users/login.html",
    authentication_form=CustomAuthenticationForm,
)
logout = django.contrib.auth.views.LogoutView.as_view(
    template_name="users/logout.html",
)
password_change = django.contrib.auth.views.PasswordChangeView.as_view(
    template_name="users/password_change.html",
    success_url=reverse_lazy("users:password_change_done"),
    form_class=CustomPasswordChangeForm,
)
password_change_done = (
    django.contrib.auth.views.PasswordChangeDoneView.as_view(
        template_name="users/password_change_done.html",
    )
)

password_reset = django.contrib.auth.views.PasswordResetView.as_view(
    template_name="users/password_reset.html",
    form_class=CustomPasswordResetForm,
)

password_reset_done = django.contrib.auth.views.PasswordResetDoneView.as_view(
    template_name="users/password_reset_done.html",
)
password_reset_confirm = (
    django.contrib.auth.views.PasswordResetConfirmView.as_view(
        template_name="users/password_reset_confirm.html",
        form_class=CustomPasswordSetForm,
    )
)
password_reset_complete = (
    django.contrib.auth.views.PasswordResetCompleteView.as_view(
        template_name="users/password_reset_complete.html",
    )
)
urlpatterns = [
    path("signup/", users.views.signup, name="signup"),
    path("user_list/", users.views.user_list, name="user_list"),
    path("user_detail/<int:pk>", users.views.user_detail, name="user_detail"),
    path("activate/<int:pk>/", users.views.activate, name="activate"),
    path("profile/", users.views.profile, name="profile"),
    path("login/", login, name="login"),
    path("logout/", logout, name="logout"),
    path("password_change/", password_change, name="password_change"),
    path("reactivate/<int:pk>", users.views.reactivate, name="reactivate"),
    path(
        "password_change/done/",
        password_change_done,
        name="password_change_done",
    ),
    path("password_reset/", password_reset, name="password_reset"),
    path(
        "password_reset/done/",
        password_reset_done,
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        password_reset_confirm,
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        password_reset_complete,
        name="password_reset_complete",
    ),
]

__all__ = []
