from django.db import models
import re
import PyPDF2
import threading
from django.contrib.auth.models import User


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


def generate_path(data, filename):
    url = "datasets/%s/%s" % (re.sub('[^a-z0-9]+', '', data.room.group_name.lower()),
                              filename)
    return url


class Data(models.Model):
    label = models.CharField(max_length=255)
    description = models.CharField(max_length=4000)
    raw_data = models.FileField(upload_to=generate_path)
    pdf_text = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    room = models.ForeignKey(Room, related_name='datasets', on_delete=models.CASCADE)
    
    def analyse_pdf(self, file_name, *args, **kwargs):
        pdfFileObj = open(self.raw_data.path, 'rb')
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        numPages = pdfReader.numPages
        print('Analysing', file_name)
        pdf_text = ""
        for np in range(numPages):
            pageObj = pdfReader.getPage(np)
            text = pageObj.extractText()
            text = text.lower()
            text = text.strip(' \t\n\r')
            if text not in ['', '\n']:
                pdf_text += text
            print('Reading page n°', np, ' on ', numPages)
        if pdf_text not in [None, '']:
            self.pdf_text = pdf_text
            self.save()
    
    def save(self, *args, **kwargs):
        file_name = self.raw_data.name
        super().save(*args, **kwargs)  # Call the "real" save() method.
        if self.pdf_text in [None, ''] and file_name.endswith('.pdf'):
            t = threading.Thread(target=self.analyse_pdf, args=file_name)
            t.daemon = True
            t.start()
    
    def __str__(self):
        return self.label
    
    def __unicode__(self):
        return '%s' % (self.label)
    
    class Meta:
        ordering = ('label',)


class Post(models.Model):
    """
    A Post.
    """
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='room_posts')
    body = models.TextField(default='')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_posts')
    type = models.IntegerField(default=0)
    answer = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True,
                               related_name='question')
    answer_to = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True,
                                  related_name='question_answer_by')
    last_editor = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True,
                                    related_name='user_last_edit')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return "<Post: {} - {} - {} >".format(self.owner.__str__(), self.room.__str__(),
                                          (self.body[:8] + '..') if len(self.body) > 10 else self.body)


class UserInRoom(models.Model):
    """
    A user connected to a room
    """
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='room_users')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_rooms')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "<UserInRoom {}: {} - {} >".format(self.pk, self.user.__str__(), self.room.__str__())
