from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from rest_framework.views import APIView
from .models import Group, User
from .serializers import GroupSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class GroupApi(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        groups = Group.objects.all()
        serializer = GroupSerializer(groups, many=True)
        return Response({'groups': serializer.data})

    def post(self, request, format=None):
        serializer = GroupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response({'group': {'id': serializer.data['id']}, 'message': 'successfull'},
                        status=status.HTTP_201_CREATED)


class MyGroupApi(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        group = Group.objects.filter(users__in=[request.user]).first()
        serializer = GroupSerializer(group)
        return Response({'groups': {'name': serializer.data['name'],
                                    'description': serializer.data['description'],
                                    'members': [
                                        {
                                            'id': user.id,
                                            'name': user.name,
                                            'email': user.email,
                                            'rule': 'Owner' if user == group.admin else 'Normal'
                                        } for user in User.objects.filter(id__in=serializer.data['users'])
                                    ]
                                    }})