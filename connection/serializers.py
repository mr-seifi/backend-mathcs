from rest_framework.serializers import ModelSerializer
from .models import JoinRequest
import json


class JoinRequestSerializer(ModelSerializer):
    class Meta:
        model = JoinRequest
        fields = ('group', 'user', 'date',)

    def __init__(self, instance=None, data=None, **kwargs):
        if data:
            req_data = json.dumps(data)
            req_data = json.loads(req_data)
            req_data['group'] = int(req_data.get('groupId'))
            super(JoinRequestSerializer, self).__init__(data=req_data)
        else:
            super(JoinRequestSerializer, self).__init__()

    def create(self, validated_data):
        join_req = JoinRequest.objects.create(group=validated_data['group'],
                                              user=validated_data['user'])

        return join_req
