from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, throttle_classes
from rest_framework import status
from accounts.serializers import UserSerializer
from rest_framework.authtoken.models import Token
from django.http import JsonResponse
from rest_framework.throttling import UserRateThrottle
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.utils import timezone
import hashlib


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


@api_view(['POST'])
@csrf_exempt
@throttle_classes([LimitPerDayUserThrottle])
def user_login(request, format='json'):
  username = request.data.get('email')
  password = request.data.get('password')
  user = authenticate(username=username, password=password)
  if user is not None:
    # the password verified for the user
    if user.is_active:
      # authenticate seems to include the is_active test
      token, created = Token.objects.get_or_create(user=user)
      request.session['auth'] = token.key
      return JsonResponse({
        "username": user.username,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "token": token.key
      }, status=status.HTTP_200_OK)
    return JsonResponse({"message": "SignIn.User_has_been_deactivated"})
  return JsonResponse({"message": "SignIn.No_user_for_the_given_email_and_password"})


@api_view(['POST'])
@csrf_exempt
@throttle_classes([LimitPerDayUserThrottle])
def user_forgetPasswordSendMail(request, format='json'):
  """
  Email
  Invalid email format
  Try if email is link to an account
  """
  user = User.objects.filter(username=request.data['email'])
  print("before test", user)
  if user.count() == 1:
    user = user.first()
    print("yessa!", user)
    now = timezone.now()
    user.userinfo.resetPasswordDate = now
    fullToken = hashlib.sha224((user.email + now.strftime("%Y-%m-%d %H:%M:%S %Z")).encode()).hexdigest()
    user.userinfo.resetPasswordToken = fullToken[0:30]
    user.save()
    print("yessa!", user, user.userinfo.resetPasswordToken, user.userinfo.resetPasswordDate)
  
  return JsonResponse({"message": 1}, status=status.HTTP_200_OK)
