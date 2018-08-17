from django.db.models.signals import post_save
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class UserInfo(models.Model):
  user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE, related_name="userinfo")
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  resetPasswordDate = models.DateTimeField(blank=True, null=True)
  resetPasswordToken = models.CharField(max_length=50, blank=True, default='')
  avatarImage = models.TextField(blank=True, default='')


# a user model was just created! This now creates your extended user (a UserInfo):
@receiver(post_save, sender=User)
def create_user_info(sender, instance, created, **kwargs):
  if created:
    UserInfo.objects.get_or_create(user=instance)


# a user model was just saved! This now save your extended user (a UserInfo):
@receiver(post_save, sender=User)
def save_user_info(sender, instance, **kwargs):
  instance.userinfo.save()


def get_user_from_token(header):
  auth = header.split()
  if not auth or auth[0].lower() != b'jwt':
    return 'Profile.unauthorized_access'
  
  if len(auth) == 1:
    return 'Invalid token header. No credentials provided.'
  
  if auth[0].lower() == b'jwt':
    token = auth[len(auth) - 1]
    # from end to get correct token when there is multiple with comma separators
    
    if token == "null":
      return 'Null token not allowed'
    
    token = token.decode("utf-8")
    gettoken = Token.objects.filter(key=token)
    if gettoken:
      user = User.objects.filter(id=gettoken[0].user_id).first()
      return user
  
  return None
