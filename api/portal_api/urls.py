from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('authentication/get_token/', obtain_auth_token, name="get_token"),
    path('register/register_user/', views.registerView.as_view(), name="register_user"),
]