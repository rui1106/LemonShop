from django.urls import path

from apps.users import login
from apps.users.login import admin_jwt_token
from apps.users.views import UserCountView, MobileCountView, Register, AddressCreateView, AddressView, Deladdress

urlpatterns = [
    path('usernames/<name>/count/', UserCountView.as_view()),
    path('mobiles/<mobile>/count/', MobileCountView.as_view()),
    path('register/', Register.as_view()),
    path('addresses/create/', AddressCreateView.as_view()),
    path('addresses/', AddressView.as_view()),
    path('addresses/<id>/', Deladdress.as_view()),
    # path('login/', LoginView.as_view()),
    path('authorizations/', login.admin_jwt_token),
]
