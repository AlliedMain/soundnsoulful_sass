from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from .custom_claims import MyTokenObtainPairView, UserProjects
from .views import registration

urlpatterns = [
    path("register/", registration),
    path("login/", MyTokenObtainPairView.as_view()),
    path("token/refresh/", TokenRefreshView.as_view()),
    path("users/", UserProjects.as_view())
]
