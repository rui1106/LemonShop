from django.urls import path

from apps.users.login import admin_jwt_token
from apps.users.views import UserCountView, MobileCountView, Register

urlpatterns = [
    path('usernames/<name>/count/', UserCountView.as_view()),
    path('mobiles/<mobile>/count/', MobileCountView.as_view()),
    path('register/', Register.as_view()),
    # path('login/', LoginView.as_view()),
    path('authorizations/', admin_jwt_token),
]
