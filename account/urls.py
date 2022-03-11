from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from .views import CustomTokenObtainPairView
from .api import RegisterApi, LoginApi

urlpatterns = [
      path('signup/', RegisterApi.as_view()),
      path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
      path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
      path('token/verify/', TokenVerifyView.as_view(), name='token_verify')
]