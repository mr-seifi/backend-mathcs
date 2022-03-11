from rest_framework import serializers
from account.models import User, Group
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('name', 'email', 'password',)
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(name=validated_data['name'],
                                        email=validated_data['email'],
                                        password=validated_data['password'])

        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password',)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    # default_error_messages = {'no_active_account': 'CUSTOM ERROR MESSAGE HERE'}  # TODO: Default error message

    def validate(self, attrs):
        data = super(CustomTokenObtainPairSerializer, self).validate(attrs)

        data['token'] = data.pop('access')
        data.pop('refresh')
        data['message'] = 'successfull'

        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['name'] = user.name
        token['email'] = user.email
        token['is_staff'] = user.is_staff

        return token


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name', 'description',)

    def create(self, validated_data):
        group = Group.objects.create(name=validated_data['name'],
                                     description=validated_data['description'],
                                     admin=validated_data['user'])
        group.users.add(validated_data['user'])

        return group
