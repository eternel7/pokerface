from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, throttle_classes
from rest_framework import status
from accounts.serializers import UserSerializer
from rest_framework.authtoken.models import Token
from django.http import JsonResponse
from rest_framework.throttling import UserRateThrottle

class LimitPerDayUserThrottle(UserRateThrottle):
        rate = '5/day'


@api_view(['POST'])
@csrf_exempt
@throttle_classes([LimitPerDayUserThrottle])
def user_create(request, format='json'):
  """
  Creates the user.
  Username
  Username already exists
  Username not provided
  Username too long
  Password
  Password not provided
  Password too short
  Email
  Email already taken
  Email not provided
  Invalid email format
  """
  serializer = UserSerializer(data=request.data)
  if serializer.is_valid(raise_exception=False):
    user = serializer.save()
    if user:
      token = Token.objects.create(user=user)
      json = serializer.data
      json['token'] = token.key
      return JsonResponse(json, status=status.HTTP_201_CREATED)

  return JsonResponse(serializer.errors)
