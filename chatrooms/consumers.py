from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from chatrooms.models import UserInRoom
from chatrooms.serializers import UserInRoomSerializer
from channels.db import database_sync_to_async
import asyncio
from .exceptions import ClientError
from .utils import get_room_or_error
import nltk
import string

# import gensim.downloader as gensim

# download the model and return as object ready for use
# model_gensim_wiki = gensim.load("glove-wiki-gigaword-100")

defaultImage = "/static/img/icons/apple-touch-icon-76x76.png"

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')
try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

lemmer = nltk.stem.WordNetLemmatizer()


def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]


remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)


def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))


class ChatConsumer(AsyncJsonWebsocketConsumer):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room_id = None
        self.rooms = None
        self.rooms_users = {}
    
    async def connect(self):
        print("websocket connection try")
        # Store which rooms the user has joined on this connection
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.rooms = set()
        
        # Are they logged in?
        if self.scope["user"].is_anonymous:
            # Reject the connection
            await self.close()
        else:
            # Accept the connection
            print("websocket accepted")
            await self.accept()
            await self.join_room(self.room_id)
    
    async def receive_json(self, content, **kwargs):
        """
        Called when we get a text frame. Channels will JSON-decode the payload
        for us and pass it as the first argument.
        """
        # Empty message so default answer
        if not content:
            await self.send_json({"text": "Welcome in my room. Let's work well together!"})
        # Messages will have a "command" key we can switch on
        command = content.get("command", None)
        
        try:
            if command == "join":
                # Make them join the room
                await self.join_room(self.room_id)
            elif command == "leave":
                # Leave the room
                await self.leave_room(self.room_id)
            elif command == "send":
                await self.send_room(self.room_id, content["message"])
            elif not command:
                pass
        except ClientError as e:
            # Catch any errors and send it back
            await self.send_json({"error": e.code})
    
    async def disconnect(self, code):
        """
        Called when the WebSocket closes for any reason.
        """
        # Leave all the rooms we are still in
        for room_id in list(self.rooms):
            try:
                await self.leave_room(room_id)
            except ClientError:
                pass
    
    # Command helper methods called by receive_json
    @database_sync_to_async
    def add_or_update_user_in_room_db(self, room_id, username):
        user_pk = User.objects.filter(username=username).first().pk
        room_pk = int(room_id)
        user_in_room = {
            "user": user_pk,
            "room": room_pk
        }
        present = UserInRoom.objects.filter(user=user_pk, room=room_pk)
        if present.count() == 0:
            serializer = UserInRoomSerializer(data=user_in_room)
            if serializer.is_valid(raise_exception=False):
                data = serializer.save()
                if data:
                    return data
            print(serializer.errors)
            return False
        else:
            now = timezone.now()
            present = present.first()
            present.updated_at = now
            present.save()
            if present:
                return present
            return False
    
    @database_sync_to_async
    def remove_user_from_room_db(self, room_id, username):
        user_pk = User.objects.filter(username=username).first().pk
        room_pk = int(room_id)
        data = UserInRoom.objects.filter(user=user_pk, room=room_pk)
        if data:
            data.delete()
            return True
        return False
    
    async def join_room(self, room_id):
        """
        Called by receive_json when someone sent a join command.
        """
        # The logged-in user is in our scope thanks to the authentication ASGI middleware
        room = await get_room_or_error(room_id, self.scope["user"])
        
        # Send a join message if it's turned on
        if settings.NOTIFY_USERS_ON_ENTER_OR_LEAVE_ROOMS:
            # send message for connecting user
            await asyncio.ensure_future(self.send_json(
                {"text": "Welcome " + self.scope["user"].username + ". I'm " + room.label +
                         ", your host in this room. What are you searching for?"})
            )
            # send message for connected users
            await asyncio.ensure_future(self.channel_layer.group_send(
                room.group_name,
                {
                    "type": "chat.join",
                    "room_id": room_id,
                    "username": self.scope["user"].username,
                }
            ))
        
        # Store that we're in the room
        self.rooms.add(room_id)
        await asyncio.ensure_future(self.add_or_update_user_in_room_db(room_id, self.scope["user"].username))
        
        # Add them to the group so they get room messages
        await asyncio.ensure_future(self.channel_layer.group_add(
            room.group_name,
            self.channel_name,
        ))
        # Instruct their client to finish opening the room
        await asyncio.ensure_future(self.send_json({
            "join": str(room.id),
            "newUser": self.scope["user"].username
        }))
    
    async def leave_room(self, room_id):
        """
        Called by receive_json when someone sent a leave command.
        """
        # The logged-in user is in our scope thanks to the authentication ASGI middleware
        room = await get_room_or_error(room_id, self.scope["user"])
        
        # Send a leave message if it's turned on
        if settings.NOTIFY_USERS_ON_ENTER_OR_LEAVE_ROOMS:
            await asyncio.ensure_future(self.channel_layer.group_send(
                room.group_name,
                {
                    "type": "chat.leave",
                    "room_id": room_id,
                    "username": self.scope["user"].username,
                }
            ))
        # Remove that we're in the room
        self.rooms.discard(room_id)
        await asyncio.ensure_future(self.remove_user_from_room_db(room_id, self.scope["user"].username))
        
        # Remove them from the group so they no longer get room messages
        await self.channel_layer.group_discard(
            room.group_name,
            self.channel_name,
        )
    
    async def send_room(self, room_id, message):
        """
        Called by receive_json when someone sends a message to a room.
        """
        # Check they are in this room
        if room_id not in self.rooms:
            raise ClientError("ROOM_ACCESS_DENIED")
        # Get the room and send to the group about it
        room = await get_room_or_error(room_id, self.scope["user"])
        
        # Update last update in room for user
        await asyncio.ensure_future(self.add_or_update_user_in_room_db(room_id, self.scope["user"].username))
        
        await self.channel_layer.group_send(
            room.group_name,
            {
                "type": "chat.message",
                "room_id": room_id,
                "username": self.scope["user"].username,
                "message": message,
            }
        )
    
    # Handlers for messages sent over the channel layer
    
    # These helper methods are named by the types we send - so chat.join becomes chat_join
    async def chat_join(self, event):
        """
        Called when someone has joined our chat.
        """
        
        # Send a message down to the client
        await self.send_json(
            {
                "msg_type": settings.MSG_TYPE_ENTER,
                "room": event["room_id"],
                "username": event["username"],
            },
        )
    
    async def chat_leave(self, event):
        """
        Called when someone has left our chat.
        """
        
        # Send a message down to the client
        await self.send_json(
            {
                "msg_type": settings.MSG_TYPE_LEAVE,
                "room": event["room_id"],
                "username": event["username"],
            },
        )
    
    async def chat_message(self, event):
        """
        Called when someone has messaged our chat.
        """
        avatar_image = await self.getuser_avatar(event["username"])
        # Send a message down to the client
        await asyncio.ensure_future(self.send_json(
            {
                "msg_type": settings.MSG_TYPE_MESSAGE,
                "room": event["room_id"],
                "username": event["username"],
                "portrait": avatar_image,
                "message": event["message"],
            },
        ))
        await asyncio.ensure_future(self.chat_bot_parse(event))
    
    async def bot_message(self, message, event):
        await asyncio.ensure_future(self.send_json(
            {
                "msg_type": settings.MSG_TYPE_MESSAGE,
                "room": event["room_id"],
                "username": 0,
                "message": message,
            },
        ))
    
    async def chat_bot_parse(self, event):
        """
        Called when someone has messaged our chat.
        One of the bot answers
        """
        # tokenize the pattern
        user_entry = event['message'].lower()
        f = open('static/chat.txt', 'r', errors='ignore')
        raw = f.read()
        raw = raw.lower()
        sent_tokens = nltk.sent_tokenize(raw)  # converts to list of sentences
        sent_tokens.append(user_entry)
        TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
        tfidf = TfidfVec.fit_transform(sent_tokens)
        vals = cosine_similarity(tfidf[-1], tfidf)
        idx = vals.argsort()[0][-2]
        flat = vals.flatten()
        flat.sort()
        req_tfidf = flat[-2]
        if (req_tfidf == 0):
            await self.bot_message("I am sorry! I don't understand you", event)
        else:
            await self.bot_message(sent_tokens[idx], event)
    
    @staticmethod
    async def getuser_avatar(username):
        # Get corresponding user avatar image
        user = User.objects.filter(username=username)
        default_image = "/static/img/icons/apple-touch-icon-76x76.png"
        if user.count() == 1:
            user = user.first()
            avatar_image = user.userinfo.avatarImage if user.userinfo and user.userinfo.avatarImage != "" else \
                default_image
            return avatar_image
        return default_image
