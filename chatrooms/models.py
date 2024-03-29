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
    raw_text = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    room = models.ForeignKey(Room, related_name='datasets', on_delete=models.CASCADE)
    
    def text_cleanup(self, text):
        text = text.lower()
        text = text.strip(' \t\n\r')
        return text

    def analyse_pdf(self, file_name, *args, **kwargs):
        pdfFileObj = open(self.raw_data.path, 'rb')
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        numPages = pdfReader.numPages
        print('Analysing', file_name)
        raw_text = ""
        for np in range(numPages):
            pageObj = pdfReader.getPage(np)
            text = pageObj.extractText()
            text = self.text_cleanup(text)
            if text not in ['', '\n']:
                raw_text += text
            print('Reading page n°', np, ' on ', numPages)
        if raw_text not in [None, '']:
            self.raw_text = raw_text
            self.save()

    def analyse_txt(self, file_name, *args, **kwargs):
        raw_text = ""
        with open(self.raw_data.path, 'r') as file:
            data = file.read().replace('\n', '')
            text = self.text_cleanup(data)
            if text not in ['', '\n']:
                raw_text += text
        if raw_text not in [None, '']:
            self.raw_text = raw_text
            self.save()
    
    def save(self, *args, **kwargs):
        file_name = self.raw_data.name
        super().save(*args, **kwargs)  # Call the "real" save() method.
        if self.raw_text in [None, ''] and file_name.endswith('.pdf'):
            t = threading.Thread(target=self.analyse_pdf, args=file_name)
            t.daemon = True
            t.start()
        if self.raw_text in [None, ''] and file_name.endswith('.txt'):
            t = threading.Thread(target=self.analyse_txt, args=file_name)
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
    body_key = models.TextField(default='')
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
    vote_count = 0
    
    def __str__(self):
        return "<Post: {} - {} - {} >".format(self.owner.__str__(), self.room.__str__(),
                                              (self.body[:8] + '..') if len(self.body) > 10 else self.body)
    
    class Meta:
        indexes = [
            models.Index(fields=['room', ]),
            models.Index(fields=['type', ]),
            models.Index(fields=['body_key', ]),
        ]


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


class ChatSyn(models.Model):
    """
    A user connected to a room
    """
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='room_synonyms')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_synonyms')
    body_key = models.TextField(default='')
    body_key_syn = models.TextField(default='')
    synonym = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return "<ChatSyn {}-{}: {} - {} >".format(self.pk, self.synonym,
                                               (self.body_key[:10] + '..') if len(self.body_key) > 14 else
                                               self.body_key,
                                               (self.body_key_syn[:10] + '..') if len(self.body_key_syn) > 14 else
                                               self.body_key_syn)
