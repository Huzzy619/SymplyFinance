from django.urls import path

from . import views

urlpatterns = [
    path("register", views.RegisterView.as_view(), name="register"),
    path(
        "login/google", views.GoogleSocialAuthView.as_view(), name="google-social-auth"
    ),
    # path('otp', views.OTPView.as_view()),
    path("login", views.LoginView.as_view(), name="login"),
    path("refresh/token", views.RefreshView.as_view(), name="token-refresh"),
    path("change/password", views.PasswordUpdateView.as_view(), name="password-update"),
    path("forgot/password", views.ForgotPasswordView.as_view(), name="forgot-password"),
    path(
        "reset/password/confirm/<uidb64>/<token>",
        views.PasswordResetConfirm.as_view(),
        name="password-reset-confirm",
    ),
]
