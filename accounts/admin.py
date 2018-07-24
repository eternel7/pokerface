from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from accounts.models import UserInfo


# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class UserInfoInline(admin.StackedInline):
  model = UserInfo
  can_delete = False
  verbose_name_plural = 'Additional information'


# Define a new User admin
class UserAdmin(BaseUserAdmin):
  inlines = (UserInfoInline, )
  
  
# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
