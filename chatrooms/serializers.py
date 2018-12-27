from rest_framework import serializers
from chatrooms.models import Room, Data


class DataSerializer(serializers.ModelSerializer):
    label = serializers.CharField(min_length=6, max_length=255)
    description = serializers.CharField(max_length=4000, required=False)
    raw_data = serializers.FileField(max_length=None, allow_empty_file=False, use_url=True)
    created_at = serializers.ReadOnlyField(source='data.created_at')
    updated_at = serializers.ReadOnlyField(source='data.updated_at')
    room = serializers.PrimaryKeyRelatedField(read_only=False,
                                              queryset=Room.objects.all())
    
    class Meta:
        model = Data
        fields = ('id', 'label', 'description', 'raw_data', 'room',
                  'created_at', 'updated_at')
        
        
class RoomSerializer(serializers.ModelSerializer):
    label = serializers.CharField(min_length=6, max_length=255)
    description = serializers.CharField(max_length=4000, required=False)
    portrait = serializers.CharField(required=False)
    image = serializers.CharField(required=False)
    staff_only = serializers.BooleanField(required=False)
    created_at = serializers.ReadOnlyField(source='room.created_at')
    updated_at = serializers.ReadOnlyField(source='room.updated_at')
    datasets = DataSerializer(many=True, read_only=True)
    
    class Meta:
        model = Room
        fields = ('id', 'label', 'description', 'portrait', 'image', 'staff_only', 'datasets',
                  'created_at', 'updated_at')
