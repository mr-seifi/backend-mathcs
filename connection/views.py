from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import JoinRequest, ConnectionRequest, Chat, Message
from .serializers import JoinRequestSerializer
from rest_framework import status
from account.models import Group, User


class JoinRequestApi(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        join_requests = JoinRequest.objects.filter(user=request.user)
        serializer = JoinRequestSerializer(join_requests, many=True)
        return Response({'joinRequests': [
            {
                'id': join_req.id,
                'groupId': join_req.group.id,
                'userId': request.user.id,
                'date': join_req.date.timestamp()
            } for join_req in request.user.join_request.all()
        ]})

    def post(self, request, *args, **kwargs):
        member = request.user.member.all()
        if not member:
            serializer = JoinRequestSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.user)
            return Response({'message': 'successfull'})
        return Response({"error": {"enMessage": "Bad request!"}},
                        status=status.HTTP_400_BAD_REQUEST)


class JoinRequestAdminApi(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if not request.user.owner.all():
            return Response({"error": {"enMessage": "Bad request!"}},
                            status=status.HTTP_400_BAD_REQUEST)

        return Response({'joinRequests': [
            {
                'id': join_request.id,
                'groupId': join_request.group.id,
                'userId': join_request.user.id,
                'date': join_request.date.timestamp()
            } for join_request in request.user.owner.first().join_request.all()
        ]})


class JoinRequestAcceptApi(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if not request.user.owner.all():
            return Response({"error": {"enMessage": "Bad request!"}},
                            status=status.HTTP_400_BAD_REQUEST)
        request_id = request.data.get('joinRequestId')
        try:
            join_request = JoinRequest.objects.get(pk=request_id)
            if join_request.group.admin != request.user:
                raise Exception()
            group: Group = request.user.owner.first()
            group.users.add(join_request.user)
            group.save()
            join_request.delete()

        except Exception as ex:
            return Response({"error": {"enMessage": "Bad request!"}},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'successfull'})


class ConnectionRequestApi(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if not request.user.owner.all():
            return Response({"error": {"enMessage": "Bad request!"}},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response({'requests': [
            {
                'connectionRequestId': connection_request.id,
                'groupId': connection_request.source_group.id,
                'sent': connection_request.sent.timestamp()
            } for connection_request in request.user.owner.first().received_request.all()
        ]})

    def post(self, request, *args, **kwargs):
        if not request.user.owner.all():
            return Response({"error": {"enMessage": "Bad request!"}},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            src_group_id = request.user.owner.first().id
            dest_group_id = request.data.get('groupId')
            connection_request = ConnectionRequest.objects.create(source_group_id=src_group_id,
                                                                  dest_group_id=dest_group_id)
        except Exception as ex:
            return Response({"error": {"enMessage": "Bad request!"}},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'successfull'})


class ConnectionRequestAcceptApi(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if not request.user.owner.all():
            return Response({"error": {"enMessage": "Bad request!"}},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            src_group_id = request.data.get('groupId')
            dest_group: Group = request.user.owner.first()
            dest_group.received_request.filter(dest_group_id=src_group_id).delete()
            dest_group.connected_groups.add(src_group_id)
            dest_group.save()
            src_group = Group.objects.get(pk=src_group_id)
            src_group.connected_groups.add(dest_group.id)
            src_group.save()

        except Exception as ex:
            return Response({"error": {"enMessage": "Bad request!"}},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'successfull'})


class ChatApi(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            return Response({'chats': [
                {
                    'userId': chat.source_user.id if chat.source_user != request.user else chat.dest_user.id,
                    'name': chat.name
                } for chat in (request.user.sent_chats.all() | request.user.received_chats.all()).distinct()
            ]})
        except Exception as ex:
            return Response({"error": {"enMessage": "Bad request!"}},
                            status=status.HTTP_400_BAD_REQUEST)


class MessageApi(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            user_id = kwargs.get('user_id')
            return Response({'chats': [
                {
                    'message': messages.text,
                    'date': messages.created,
                    'sentby': messages.chat.source_user.id
                } for messages in Message.objects.filter(chat__source_user=request.user,
                                                         chat__dest_user_id=user_id)
            ]})
        except Exception as ex:
            return Response({"error": {"enMessage": "Bad request!"}},
                            status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        try:
            user_id = kwargs.get('user_id')
            dest_user = User.objects.get(pk=user_id)
            chat = Chat.objects.filter(source_user=request.user,
                                       dest_user_id=user_id).first()
            if not chat:
                if request.user.member.first().id in dest_user.member.first().connected_groups.all():
                    chat = Chat.objects.create(source_user=request.user,
                                               dest_user=dest_user,
                                               name='default')
                else:
                    raise Exception()

            message = Message.objects.create(text=request.data.get('message'))
            chat.messages.add(message.id)
            chat.save()

        except Exception as ex:
            return Response({"error": {"enMessage": "Bad request!"}},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'successfull'})

