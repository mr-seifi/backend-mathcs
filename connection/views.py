from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import JoinRequest
from .serializers import JoinRequestSerializer
from rest_framework import status
from account.models import Group


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
