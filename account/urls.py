from django.urls import path
from .views import CustomTokenObtainPairView, GroupApi, MyGroupApi
from .api import RegisterApi

urlpatterns = [
      path('auth/signup/', RegisterApi.as_view()),
      path('auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
      path('groups/', GroupApi.as_view(), name='groups'),
      path('groups/my/', MyGroupApi.as_view(), name='my_groups')
]
