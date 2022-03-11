from django.urls import path
from .views import JoinRequestApi, JoinRequestAdminApi, JoinRequestAcceptApi

# TODO: Route
urlpatterns = [
    path('join_requests/', JoinRequestApi.as_view(), name='join_requests'),
    path('join_requests/group/', JoinRequestAdminApi.as_view(), name='join_request_admin'),
    path('join_requests/accept/', JoinRequestAcceptApi.as_view(), name='join_request_accept')
]
