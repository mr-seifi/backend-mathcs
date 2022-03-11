from django.urls import path
from .views import JoinRequestApi, JoinRequestAdminApi, JoinRequestAcceptApi,\
    ConnectionRequestApi, ConnectionRequestAcceptApi

# TODO: Route
urlpatterns = [
    path('join_requests/', JoinRequestApi.as_view(), name='join_requests'),
    path('join_requests/group/', JoinRequestAdminApi.as_view(), name='join_request_admin'),
    path('join_requests/accept/', JoinRequestAcceptApi.as_view(), name='join_request_accept'),
    path('connection_requests/', ConnectionRequestApi.as_view(), name='connection_request'),
    path('connection_requests/accept/', ConnectionRequestAcceptApi.as_view(), name='connection_request_accept')

]
