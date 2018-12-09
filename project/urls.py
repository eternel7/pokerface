"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import re_path, include
from django.contrib import admin
from .views import HomePageView, check_token
from accounts import views as account_views
from chatrooms import views as chatrooms_views
from chatrooms import apps

urlpatterns = [
  re_path(r'^admin/', admin.site.urls),
  re_path(r'^api/login/', include('rest_social_auth.urls_jwt')),
  re_path(r'^api/login/', include('rest_social_auth.urls_token')),
  re_path(r'^api/login/', include('rest_social_auth.urls_session')),
  re_path(r'^auth/', include('rest_framework_social_oauth2.urls')),
  re_path(r'api/check/', check_token),
  re_path(r'^api/ulogout/', account_views.user_logOut, name='logoutUser'),
  re_path(r'^auth/register', account_views.user_create, name='signUp'),
  re_path(r'^auth/login', account_views.user_login, name='signIn'),
  re_path(r'^fpwd', account_views.user_forgetPasswordSendMail, name='forgetPasswordSendMail'),
  re_path(r'^rpwd', account_views.user_resetPassword, name='resetPassword'),
  re_path(r'^upwd', account_views.user_updatePassword, name='updatePassword'),
  re_path(r'^api/uuser/', account_views.user_update, name='updateUser'),
  re_path(r'^api/guser/', account_views.user_get, name='getUser'),
  re_path(r'^api/duser/', account_views.user_delete, name='deleteUser'),
  re_path(r'^api/chatrooms/', chatrooms_views.chatrooms_get, name='getChatrooms'),
  re_path(r'^api/chatterbot/', chatrooms_views.chat_post, name='chatterbot'),
  re_path(r'^$', HomePageView.as_view(), name='home'),
]

# migrate chatterBot before uncomment
# apps.init_chatbot()
