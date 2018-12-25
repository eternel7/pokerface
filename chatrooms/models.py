from django.db import models


class Room(models.Model):
    """
    A room for people to chat in.
    """
    
    # Room title
    label = models.CharField(max_length=255)
    description = models.CharField(max_length=4000)
    portrait = models.TextField()
    image = models.TextField()
    
    # If only "staff" users are allowed (is_staff on django's User)
    staff_only = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.label
    
    @property
    def group_name(self):
        """
        Returns the Channels Group name that sockets should subscribe to to get sent
        messages as they are generated.
        """
        return "room-%s" % self.id
