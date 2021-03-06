from rest_framework import serializers
from chatrooms.models import Room, Data, Post, UserInRoom, ChatSyn
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    avatar_image = serializers.CharField(source='userinfo.avatarImage', required=False)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'id', 'avatar_image', 'last_name', 'first_name')


class DataSerializer(serializers.ModelSerializer):
    label = serializers.CharField(min_length=3, max_length=255)
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
    label = serializers.CharField(min_length=3, max_length=255)
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


class PostSerializer(serializers.ModelSerializer):
    body = serializers.CharField(required=True)
    owner = serializers.PrimaryKeyRelatedField(allow_null=False,
                                               allow_empty=False,
                                               read_only=False,
                                               queryset=User.objects.all())
    last_editor = serializers.PrimaryKeyRelatedField(required=False,
                                                     allow_null=True,
                                                     allow_empty=True,
                                                     read_only=False,
                                                     queryset=User.objects.all())
    answer = serializers.PrimaryKeyRelatedField(required=False,
                                                allow_null=True,
                                                allow_empty=True,
                                                read_only=False,
                                                queryset=Post.objects.all())
    answer_to = serializers.PrimaryKeyRelatedField(required=False,
                                                   allow_null=True,
                                                   allow_empty=True,
                                                   read_only=False,
                                                   queryset=Post.objects.all())
    room = serializers.PrimaryKeyRelatedField(required=True,
                                              read_only=False,
                                              queryset=Room.objects.all())
    
    class Meta:
        model = Post
        fields = ('id', 'body', 'owner', 'answer', 'answer_to', 'last_editor', 'room',
                  'created_at', 'updated_at')


class AnswerSerializer(serializers.ModelSerializer):
    body = serializers.CharField(required=True)
    owner = UserSerializer(allow_null=False, read_only=True)
    last_editor = UserSerializer(allow_null=False, read_only=True)
    answer_to = serializers.PrimaryKeyRelatedField(required=False,
                                                   allow_null=True,
                                                   allow_empty=True,
                                                   read_only=False,
                                                   queryset=Post.objects.all())
    room = serializers.PrimaryKeyRelatedField(required=True,
                                              read_only=False,
                                              queryset=Room.objects.all())
    
    class Meta:
        model = Post
        fields = ('id', 'body', 'owner', 'answer_to', 'last_editor', 'room', 'vote_count',
                  'created_at', 'updated_at')


class QuestionSerializer(serializers.ModelSerializer):
    body = serializers.CharField(required=True)
    owner = UserSerializer(allow_null=False, read_only=True)
    last_editor = UserSerializer(allow_null=False, read_only=True)
    answer = serializers.PrimaryKeyRelatedField(required=False,
                                                allow_null=True,
                                                allow_empty=True,
                                                read_only=False,
                                                queryset=Post.objects.all())
    answer_to = serializers.PrimaryKeyRelatedField(required=False,
                                                   allow_null=True,
                                                   allow_empty=True,
                                                   read_only=False,
                                                   queryset=Post.objects.all())
    room = serializers.PrimaryKeyRelatedField(required=True,
                                              read_only=False,
                                              queryset=Room.objects.all())
    answers = serializers.SerializerMethodField()
    
    @staticmethod
    def get_answers(obj):
        list_answers = Post.objects.filter(answer_to=obj.pk)
        if list_answers.count() > 0:
            return AnswerSerializer(list_answers, many=True).data
        return []
    
    class Meta:
        model = Post
        fields = ('id', 'body', 'owner', 'answer', 'answer_to', 'last_editor', 'room', 'vote_count',
                  'answers', 'created_at', 'updated_at')


class UserInRoomSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(allow_null=False,
                                              allow_empty=False,
                                              read_only=False,
                                              queryset=User.objects.all())
    room = serializers.PrimaryKeyRelatedField(required=True,
                                              read_only=False,
                                              queryset=Room.objects.all())
    
    class Meta:
        model = UserInRoom
        fields = ('id', 'user', 'room', 'created_at', 'updated_at')


class UserInRoomReadSerializer(serializers.ModelSerializer):
    user_obj = UserSerializer(allow_null=False, read_only=True, source='user')
    room = serializers.PrimaryKeyRelatedField(read_only=True)
    
    class Meta:
        model = UserInRoom
        fields = ('id', 'user_obj', 'room', 'created_at', 'updated_at')


class ChatSynSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(allow_null=False,
                                              allow_empty=False,
                                              read_only=False,
                                              queryset=User.objects.all())
    room = serializers.PrimaryKeyRelatedField(required=True,
                                              read_only=False,
                                              queryset=Room.objects.all())
    body_key = serializers.CharField(required=True)
    body_key_syn = serializers.CharField(required=True)
    synonym = serializers.BooleanField(required=True)
    
    class Meta:
        model = ChatSyn
        fields = ('id', 'user', 'room', 'synonym', 'body_key', 'body_key_syn',
                  'created_at', 'updated_at')
