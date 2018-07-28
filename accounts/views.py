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
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from django_user_agents.utils import get_user_agent


class LimitPerDayUserThrottle(UserRateThrottle):
  rate = '10/day'


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
  email = request.data['email']
  user = User.objects.filter(username=email)
  print("before test", user)
  if user.count() == 1:
    user = user.first()
    print("yessa!", user.email)
    now = timezone.now()
    user.userinfo.resetPasswordDate = now + timezone.timedelta(hours=2)
    fullToken = hashlib.sha224((user.email + now.strftime("%Y-%m-%d %H:%M:%S %Z")).encode()).hexdigest()
    user.userinfo.resetPasswordToken = fullToken[0:30]
    user.save()
    print("user ready for password update => sending information by mail")
    user_agent = get_user_agent(request)
    infos = {'resetPasswordToken': user.userinfo.resetPasswordToken,
             'title': "Reset password for PokerFace",
             'first_name': user.first_name,
             'last_name': user.last_name,
             'email': email,
             'action_url': 'http://localhost:8000/#/resetpassword/' + user.userinfo.resetPasswordToken,
             'support_url': 'http://localhost:8000/#/support',
             'name': user.first_name if user.first_name != "" else email,
             'operating_system': user_agent.os.family,
             'ip_address': request.META['REMOTE_ADDR'],
             'browser_name': user_agent.browser.family}
    msg_plain = render_to_string('../templates/project/emails/forgotpassword.txt', infos)
    msg_html = render_to_string('../templates/project/emails/forgotpassword.html', infos)
    print('sending reset password instructions...')
    send_mail('Reset password for PokerFace',
              msg_plain,
              settings.EMAIL_HOST_USER,
              [email],
              html_message=msg_html,
              fail_silently=True,
              )
    print("send!!")
  if not user:
    infos = {'email': email,
             'support_url': 'http://localhost:8000/#/support',
             'operating_system': request.META['HTTP_USER_AGENT'],
             'ip_address': request.META['REMOTE_ADDR'],
             'browser_name': request.META['HTTP_USER_AGENT']}
    msg_plain = render_to_string('../templates/project/emails/forgotpasswordnoaccount.txt', infos)
    msg_html = render_to_string('../templates/project/emails/forgotpasswordnoaccount.html', infos)
    print('sending reset password ask to unknown account...')
    send_mail('Reset password on PokerFace but we don\'t know you',
              msg_plain,
              settings.EMAIL_HOST_USER,
              [email],
              html_message=msg_html,
              fail_silently=False,
              )
    print("send!!")
  return JsonResponse({"message": 1}, status=status.HTTP_200_OK)


@api_view(['POST'])
@csrf_exempt
@throttle_classes([LimitPerDayUserThrottle])
def user_resetPassword(request, format='json'):
  """
  Email
  Invalid email format
  Try if email is link to an account
  """
  email = request.data['email']
  password = request.data['password']
  confirmPassword = request.data['confirmPassword']
  resetPasswordToken = request.data['resetPasswordToken']
  user = User.objects.filter(username=email)
  print("before test", user)
  if user.count() == 1:
    user = user.first()
    print("found user!", user.email)
    if len(password) >= 6 and password == confirmPassword:
      if len(user.userinfo.resetPasswordToken) == 30 and user.userinfo.resetPasswordToken == resetPasswordToken:
        now = timezone.now()
        print("user token correct!", user.email, user.userinfo.resetPasswordDate, now)
        if user.userinfo.resetPasswordDate >= now:
          print("user ready for password update")
          user.set_password(password)
          user.userinfo.resetPasswordToken = ""
          user.userinfo.resetPasswordDate = now + timezone.timedelta(days=-365)
          user.save()
          print("user password updated! Token set to invalid.")
          user_agent = get_user_agent(request)
          infos = {'resetPasswordToken': user.userinfo.resetPasswordToken,
                   'title': "Your password has been reset successfully for PokerFace",
                   'first_name': user.first_name,
                   'last_name': user.last_name,
                   'email': email,
                   'action_url': 'http://localhost:8000/#/signin',
                   'support_url': 'http://localhost:8000/#/support',
                   'name': user.first_name if user.first_name != "" else email,
                   'operating_system': user_agent.os.family,
                   'ip_address': request.META['REMOTE_ADDR'],
                   'browser_name': user_agent.browser.family}
          msg_plain = render_to_string('../templates/project/emails/passwordhasbeenreset.txt', infos)
          msg_html = render_to_string('../templates/project/emails/passwordhasbeenreset.html', infos)
          print('sending reset password confirmation mail.')
          send_mail('Your password has been reset successfully for PokerFace',
                    msg_plain,
                    settings.EMAIL_HOST_USER,
                    [email],
                    html_message=msg_html,
                    fail_silently=True,
                    )
          print("send!!")
          return JsonResponse({"state": 1, "message": "ResetPassword.Reset_done_trying_automatic_log_in"},
                              status=status.HTTP_200_OK)
        print("user token not valid anymore", user.email)
        return JsonResponse({"message": "ResetPassword.Security_token_no_more_valid"}, status=status.HTTP_200_OK)
      print("user token incorrect", user.email)
      return JsonResponse({"message": "ResetPassword.Security_token_invalid"}, status=status.HTTP_200_OK)
    print("password not identical to password confirmation", user.email)
    return JsonResponse({"message": "SignUp.ConfirmedPasswordIncorrect"}, status=status.HTTP_200_OK)
  print("no user found for this email", email)
  return JsonResponse({"message": "ResetPassword.no_user_found_for_this_email"}, status=status.HTTP_200_OK)
