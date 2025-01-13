from django.urls import path
from .views import *
urlpatterns = [
    path("register/user/",RegisterUserAPIView.as_view(),name='register'),
    path("login/user/",LoginUserAPIView.as_view(),name='login')
]

