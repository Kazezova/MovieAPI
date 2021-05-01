from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token
from auth_.views import UserCreateView

urlpatterns = [
    path('login/', obtain_jwt_token),
    path('register/', UserCreateView.as_view())
]
