from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from .views import CustomTokenObtainPairView, GroupApi
from .api import RegisterApi, LoginApi

urlpatterns = [
      path('auth/signup/', RegisterApi.as_view()),
      path('auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
      path('groups/', GroupApi.as_view(), name='groups')
]