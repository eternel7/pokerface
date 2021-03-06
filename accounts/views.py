from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, throttle_classes
from rest_framework import status
from accounts.serializers import UserSerializer
from accounts.models import get_user_from_token
from rest_framework.authtoken.models import Token
from rest_framework.authentication import get_authorization_header
from django.http import JsonResponse
from rest_framework.throttling import UserRateThrottle
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.utils import timezone
import hashlib
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from django_user_agents.utils import get_user_agent
from project.tools import format_translations

import json

defaultImage = "/static/img/icons/apple-touch-icon-76x76.png"


class LimitPerDayUserThrottle(UserRateThrottle):
  rate = '5555/hour'

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
      json['avatar_image'] = user.userinfo.avatarImage
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
      login(request, user)
      print('login', request.user)
      # authenticate seems to include the is_active test
      token, created = Token.objects.get_or_create(user=user)
      request.session['auth'] = token.key
      avatar_image = user.userinfo.avatarImage if user.userinfo and user.userinfo.avatarImage != "" else defaultImage
      return JsonResponse({
        "username": user.username,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "avatar_image": avatar_image,
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
  if user.count() == 1:
    user = user.first()
    now = timezone.now()
    user.userinfo.resetPasswordDate = now + timezone.timedelta(hours=2)
    fullToken = hashlib.sha224((user.email + now.strftime("%Y-%m-%d %H:%M:%S %Z")).encode()).hexdigest()
    user.userinfo.resetPasswordToken = fullToken[0:30]
    user.save()
    print("user ready for password update => sending information by mail")
    user_agent = get_user_agent(request)
    infos = {'resetPasswordToken': user.userinfo.resetPasswordToken,
             'first_name': user.first_name,
             'last_name': user.last_name,
             'email': email,
             'action_url': request.build_absolute_uri('/#/resetpassword/' + user.userinfo.resetPasswordToken),
             'support_url': request.build_absolute_uri('/#/support'),
             'name': user.first_name if user.first_name != "" else email,
             'operating_system': user_agent.os.family,
             'ip_address': request.META['REMOTE_ADDR'],
             'browser_name': user_agent.browser.family}
    emailTitle = 'Request to reset password'
    lang = request.data['language']
    if lang:
      json_data = open('static/translations/' + lang + '.json', encoding='utf-8')
      translation_data = json.load(json_data)
      json_data.close()
      infos['t'] = translation_data['emails']['forgotPassword']
      emailTitle = infos['t']['headTitle']
      infos['t'] = format_translations(infos, 't')
    msg_plain = render_to_string('../templates/project/emails/forgotpassword.txt', infos)
    msg_html = render_to_string('../templates/project/emails/forgotpassword.html', infos)
    print('sending reset password instructions...', request.build_absolute_uri('/#/support'))
    send_mail(emailTitle,
              msg_plain,
              settings.EMAIL_HOST_USER,
              [email],
              html_message=msg_html,
              fail_silently=True,
              )
    print("send.")
  if not user:
    user_agent = get_user_agent(request)
    infos = {'email': email,
             'name': email,
             'support_url': request.build_absolute_uri('/#/support'),
             'operating_system': user_agent.os.family,
             'ip_address': request.META['REMOTE_ADDR'],
             'browser_name': user_agent.browser.family}
    emailTitle = 'Reset password on PokerFace but we don\'t know you'
    lang = request.data['language']
    if lang:
      json_data = open('static/translations/' + lang + '.json', encoding='utf-8')
      translation_data = json.load(json_data)
      json_data.close()
      infos['LANGUAGE_CODE'] = lang
      infos['t'] = translation_data['emails']['forgotpasswordnoaccount']
      emailTitle = infos['t']['headTitle']
      infos['t'] = format_translations(infos, 't')
    msg_plain = render_to_string('../templates/project/emails/forgotpasswordnoaccount.txt', infos)
    msg_html = render_to_string('../templates/project/emails/forgotpasswordnoaccount.html', infos)
    print('sending reset password ask to unknown account...')
    send_mail(emailTitle,
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
def user_updatePassword(request, format='json'):
  """
  Confirmed new password
  Update user password
  Send email of update confirmation
  """
  
  user = get_user_from_token(get_authorization_header(request))
  
  if isinstance(user, str):
    print("message for user", user, " in user_updatePassword")
    return JsonResponse({"message": user}, status=status.HTTP_200_OK)
  
  if user:
    email = request.data['email']
    password = request.data['password']
    newPassword = request.data['newPassword']
    confirmPassword = request.data['confirmPassword']
    testUser = authenticate(username=email, password=password)
    print("authenticated user", user, testUser)
    if user.email == email and testUser is not None:
      if len(newPassword) >= 6 and newPassword == confirmPassword:
        user.set_password(newPassword)
        user.save()
        user_agent = get_user_agent(request)
        infos = {'first_name': user.first_name,
                 'last_name': user.last_name,
                 'email': email,
                 'action_url': request.build_absolute_uri('/#/signin'),
                 'support_url': request.build_absolute_uri('/#/support'),
                 'name': user.first_name if user.first_name != "" else email,
                 'operating_system': user_agent.os.family,
                 'ip_address': request.META['REMOTE_ADDR'],
                 'browser_name': user_agent.browser.family}
        emailTitle = 'Your password has been updated successfully for PokerFace'
        lang = request.data['language']
        if lang:
          json_data = open('static/translations/' + lang + '.json', encoding='utf-8')
          translation_data = json.load(json_data)
          json_data.close()
          infos['t'] = translation_data['emails']['passwordhasbeenupdated']
          emailTitle = infos['t']['headTitle']
          infos['t'] = format_translations(infos, 't')
        msg_plain = render_to_string('../templates/project/emails/passwordhasbeenupdated.txt', infos)
        msg_html = render_to_string('../templates/project/emails/passwordhasbeenupdated.html', infos)
        print('sending update password confirmation mail.')
        send_mail(emailTitle,
                  msg_plain,
                  settings.EMAIL_HOST_USER,
                  [email],
                  html_message=msg_html,
                  fail_silently=True,
                  )
        print("send!!")
        return JsonResponse({"state": 1,
                             "message": "user.Password_updated"}, status=status.HTTP_200_OK)
      return JsonResponse({"message": "user.New_password_not_correctly_confirmed_or_too_short"})
    return JsonResponse({"message": "user.Wrong_former_password"})
  return JsonResponse({"message": "user.Your_not_authenticated"})


@api_view(['POST'])
@csrf_exempt
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
  if user.count() == 1:
    user = user.first()
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
                   'first_name': user.first_name,
                   'last_name': user.last_name,
                   'email': email,
                   'action_url': request.build_absolute_uri('/#/signin'),
                   'support_url': request.build_absolute_uri('/#/support'),
                   'name': user.first_name if user.first_name != "" else email,
                   'operating_system': user_agent.os.family,
                   'ip_address': request.META['REMOTE_ADDR'],
                   'browser_name': user_agent.browser.family}
          emailTitle = 'Your password has been reset successfully for PokerFace'
          lang = request.data['language']
          if lang:
            json_data = open('static/translations/' + lang + '.json', encoding='utf-8')
            translation_data = json.load(json_data)
            json_data.close()
            infos['t'] = translation_data['emails']['passwordhasbeenreset']
            emailTitle = infos['t']['headTitle']
            infos['t'] = format_translations(infos, 't')
          msg_plain = render_to_string('../templates/project/emails/passwordhasbeenreset.txt', infos)
          msg_html = render_to_string('../templates/project/emails/passwordhasbeenreset.html', infos)
          print('sending reset password confirmation mail.')
          send_mail(emailTitle,
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


@api_view(['PUT'])
@csrf_exempt
def user_update(request, format='json'):
  user = get_user_from_token(get_authorization_header(request))
  
  if isinstance(user, str):
    print("message for user", user)
    return JsonResponse({"message": user}, status=status.HTTP_200_OK)
  
  if user:
    print("authenticated user", user)
    user.first_name = request.data['first_name']
    user.last_name = request.data['last_name']
    avatar_image = request.data['avatar_image']
    if avatar_image.startswith("data:image/"):
      user.userinfo.avatarImage = avatar_image
    else:
      user.userinfo.avatarImage = defaultImage
    if user.email == "":
      user.email = request.data['email']
    
    user.save()
    return JsonResponse({"message": "Profile.Update_done",
                         "user": {"email": user.email,
                                  "username": user.email,
                                  "first_name": user.first_name,
                                  "last_name": user.last_name,
                                  "avatar_image": user.userinfo.avatarImage,
                                  }}, status=status.HTTP_200_OK)
  print("unauthenticated user", request.user)
  return JsonResponse({"message": "Profile.unauthorized_access"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@csrf_exempt
def user_logOut(request, format='json'):
  if request.user and request.user.is_authenticated:
    logout(request)
    return JsonResponse({"message": "user.Logout"}, status=status.HTTP_200_OK)
  print("logout unauthenticated user")
  return JsonResponse({"message": "user.nonConnected"}, status=status.HTTP_200_OK)


@api_view(['GET'])
@csrf_exempt
def user_get(request, format='json'):
  user = get_user_from_token(get_authorization_header(request))
  if user:
    social_info = None
    social_set = user.social_auth.values_list('provider')
    if social_set:
      for social in social_set:
        social_info = social[0]
    
    avatar_image = user.userinfo.avatarImage if user.userinfo and user.userinfo.avatarImage != "" else defaultImage
    return JsonResponse({"user":
                           {"email": user.email,
                            "username": user.username,
                            "first_name": user.first_name,
                            "last_name": user.last_name,
                            "avatar_image": avatar_image,
                            "social_info": social_info,
                            }}, status=status.HTTP_200_OK)
  
  return JsonResponse({"message": "user.nonConnected"}, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@csrf_exempt
def user_delete(request, format='json'):
  user = get_user_from_token(get_authorization_header(request))
  if user:
    email = user.email
    user.delete()
    return JsonResponse({"email": email}, status=status.HTTP_200_OK)
  
  return JsonResponse({"message": "user.nonConnected"}, status=status.HTTP_200_OK)
