from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from .api import RegisterApi

urlpatterns = [
      path('signup/', RegisterApi.as_view()),
      path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
      path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
      path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify')
]