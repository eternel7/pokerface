from django.db.models.signals import post_save
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver


class UserInfo(models.Model):
  user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE, related_name="userinfo")
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  resetPasswordDate = models.DateTimeField(blank=True, null=True)
  resetPasswordToken = models.CharField(max_length=50, blank=True, default='')


# a user model was just created! This now creates your extended user (a UserInfo):
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
  if created:
    UserInfo.objects.get_or_create(user=instance)
