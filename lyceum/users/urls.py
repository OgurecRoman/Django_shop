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

urlpatterns = [
    path("signup/", users.views.signup, name="signup"),
    path("login/",
         django.contrib.auth.views.LoginView.as_view(
             template_name="users/login.html",
             authentication_form=CustomAuthenticationForm, ),
         name="login", ),

    path("logout/",
         django.contrib.auth.views.LogoutView.as_view(),
         name="logout", ),

    path("password_change/",
         django.contrib.auth.views.PasswordChangeView.as_view(
             template_name="users/password_change.html",
             success_url=reverse_lazy("users:password_change_done"),
             form_class=CustomPasswordChangeForm, ),
         name="password_change", ),

    path("password_change/done/",
         django.contrib.auth.views.PasswordChangeDoneView.as_view(
             template_name="users/password_change_done.html", ),
         name="password_change_done", ),
    path("password_reset/",
         django.contrib.auth.views.PasswordResetView.as_view(
             template_name="users/password_reset.html",
             form_class=CustomPasswordResetForm, ),
         name="password_reset", ),
    path("password_reset/done/",
         django.contrib.auth.views.PasswordResetDoneView.as_view(
             template_name="users/password_reset_done.html", ),
         name="password_reset_done", ),

    path("reset/<uidb64>/<token>/",
         django.contrib.auth.views.PasswordResetConfirmView.as_view(
             template_name="users/password_reset_confirm.html",
             form_class=CustomPasswordSetForm, ),
         name="password_reset_confirm", ),

    path("user_list/",
         users.views.user_list,
         name="user_list",
         ),
    path(
        "user_detail/",
        users.views.user_detail,
        name="user_detail",
    ),
    path(
        "/activate/<str:username>/",
        users.views.activate,
        name="activate",
    ),
]

__all__ = []
