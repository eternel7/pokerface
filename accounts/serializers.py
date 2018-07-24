from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from accounts.models import UserInfo


class UserSerializer(serializers.ModelSerializer):
  email = serializers.EmailField(
    required=True,
    validators=[UniqueValidator(queryset=User.objects.all())]
  )
  password = serializers.CharField(min_length=6, write_only=True)
  created_at = serializers.ReadOnlyField(source='userinfo.created_at')
  updated_at = serializers.ReadOnlyField(source='userinfo.updated_at')
  resetPasswordDate = serializers.DateTimeField(source='userinfo.resetPasswordDate', read_only=True)
  resetPasswordToken = serializers.DateTimeField(source='userinfo.resetPasswordToken', read_only=True)
  
  def create(self, validated_data):
    user = User.objects.create_user(validated_data['email'], validated_data['email'],
                                    validated_data['password'])
    return user
  
  class Meta:
    model = User
    fields = ('id', 'username', 'email', 'password',
              'created_at', 'updated_at',
              'resetPasswordDate', 'resetPasswordToken')
