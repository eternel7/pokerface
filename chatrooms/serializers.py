from rest_framework import serializers
from chatrooms.models import Room


class RoomSerializer(serializers.ModelSerializer):
    label = serializers.CharField(min_length=6, max_length=255)
    description = serializers.CharField(max_length=4000, required=False)
    portrait = serializers.CharField(required=False)
    image = serializers.CharField(required=False)
    staff_only = serializers.BooleanField(required=False)
    created_at = serializers.ReadOnlyField(source='userinfo.created_at')
    updated_at = serializers.ReadOnlyField(source='userinfo.updated_at')
    
    class Meta:
        model = Room
        fields = ('id', 'label', 'description', 'portrait', 'image', 'staff_only',
                  'created_at', 'updated_at')
