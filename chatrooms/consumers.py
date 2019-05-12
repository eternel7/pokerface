from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from chatrooms.models import UserInRoom, Post
from chatrooms.serializers import UserInRoomSerializer
from chatrooms.views import create_or_update_post
from channels.db import database_sync_to_async
from chatrooms.queries import get_answer_text_to_question, get_first_answer_text_to_question_keys
from chatrooms.queries import get_all_validated_questions_texts, get_all_validated_questions_keys
import asyncio
from .exceptions import ClientError
from .utils import get_room_or_error
from chatrooms.nlp import findClosestText, cleanText, textToKeys
import json

defaultImage = "/static/img/icons/apple-touch-icon-76x76.png"


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
                await self.send_room(self.room_id, content["message"], content["lang"])
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
    
    # Command helper methods
    @classmethod
    def getuser(cls, username):
        user = User.objects.filter(username=username)
        if user.count() == 1:
            user = user.first()
            return user
        return None
    
    @classmethod
    def getuser_pk(cls, username):
        user = cls.getuser(username)
        if user:
            return user.pk
        return None
    
    @staticmethod
    async def getuser_avatar(username):
        # Get corresponding user avatar image
        user = ChatConsumer.getuser(username)
        default_image = "/static/img/icons/apple-touch-icon-76x76.png"
        if user:
            avatar_image = user.userinfo.avatarImage if user.userinfo and user.userinfo.avatarImage != "" else default_image
            return avatar_image
        return default_image
    
    @database_sync_to_async
    def add_or_update_user_in_room_db(self, room_id, username):
        user_pk = ChatConsumer.getuser_pk(username)
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
            print("add_or_update_user_in_room_db", serializer.errors)
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
        user_pk = ChatConsumer.getuser_pk(username)
        room_pk = int(room_id)
        data = UserInRoom.objects.filter(user=user_pk, room=room_pk)
        if data:
            data.delete()
            return True
        return False
    
    @database_sync_to_async
    def add_or_update_post_in_room_db(self, room_id, username, message, type_num=1, post_id=None, lang="french"):
        user = ChatConsumer.getuser(username)
        data = {
            "message": message,
            "type": int(type_num),
            "room": int(room_id)
        }
        if post_id:
            data.post_id = post_id
        
        post = create_or_update_post(user, data, lang)
        
        if post.pk:
            return post.pk
        return post
    
    @database_sync_to_async
    def get_all_validated_questions_texts(self):
        return get_all_validated_questions_texts()
    
    @database_sync_to_async
    def get_all_validated_questions_keys(self):
        return get_all_validated_questions_keys()
    
    @database_sync_to_async
    def get_first_validated_question_for_keys(self, textkeys):
        q = Post.objects.filter(body_key=textkeys, type=1).exclude(answer__isnull=True)
        if q.count() > 0:
            return q[0].body
    
    @database_sync_to_async
    def get_first_answer_text_to_question(self, question):
        response = get_answer_text_to_question(question)
        if response:
            return response
        return None
    
    @database_sync_to_async
    def get_first_answer_text_to_question_keys(self, textkeys):
        response = get_first_answer_text_to_question_keys(textkeys)
        print("response", response, textkeys)
        if response:
            return response
        return None
    
    @database_sync_to_async
    def update_all_keys(self, lang):
        posts = Post.objects.exclude(answer__isnull=True)
        for p in posts:
            Post.objects.filter(pk=p.pk).update(body_key=json.dumps(textToKeys(p.body, 'french')))
    
    async def join_room(self, room_id):
        """
        Called by receive_json when someone sent a join command.
        """
        # The logged-in user is in our scope thanks to the authentication ASGI middleware
        room = await get_room_or_error(room_id, self.scope["user"])
        
        # Send a join message if it's turned on
        if settings.NOTIFY_USERS_ON_ENTER_OR_LEAVE_ROOMS:
            # send message for connecting user
            await asyncio.ensure_future(self.bot_message({
                "msg": "room.WelcomeInTheRoom",
                "user": self.scope["user"].username,
                "room_label": room.label
            }, {"room_id": room_id}))
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
    
    async def send_room(self, room_id, message, lang):
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
        
        # Store post in DB to set it post_id
        post_id = await self.add_or_update_post_in_room_db(room_id, self.scope["user"].username, message, 1, None, lang)
        
        await self.channel_layer.group_send(
            room.group_name,
            {
                "type": "chat.message",
                "room_id": room_id,
                "username": self.scope["user"].username,
                "message": message,
                "post_id": post_id,
                "lang": lang
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
                "post_id": event["post_id"],
                "lang": event["lang"]
            },
        ))
        if 'no_bot' not in event:
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
    
    async def chat_bot_message(self, event):
        await asyncio.ensure_future(self.send_json(
            {
                "msg_type": settings.MSG_TYPE_MESSAGE,
                "room": event["room_id"],
                "username": 0,
                "message": event["message"],
            },
        ))
    
    async def send_data(self, event):
        await asyncio.ensure_future(self.send_json(
            {
                "msg_type": settings.MSG_TYPE_DATA,
                "room": event["room_id"],
                "username": 0,
                "class": event["class"],
                "data": event["data"],
            },
        ))
    
    async def send_info(self, event):
        await asyncio.ensure_future(self.send_json(
            {
                "msg_type": settings.MSG_TYPE_INFO,
                "room": event["room_id"],
                "username": 0,
                "message": event["message"],
            },
        ))
    
    async def chat_bot_parse(self, event):
        """
        Called when someone has messaged our chat.
        One of the bot answers
        """
        user_entry = event['message']
        first_try = await asyncio.ensure_future(self.closest_to_answered_question(user_entry, event))
        if not first_try:
            await asyncio.ensure_future(self.text_to_keys_question(user_entry, event))
    
    async def closest_to_answered_question(self, user_entry, event):
        text = cleanText(user_entry)
        questions = await self.get_all_validated_questions_texts()
        if questions.count() > 0:
            closest = findClosestText(text, list(questions))
            if closest:
                print('closest_to_answered_question', event['message'], text, closest)
                if closest["score"] >= 0.8:
                    response = await self.get_first_answer_text_to_question(closest["text"])
                    await self.bot_message(response, event)
                    return True
        return None
    
    async def text_to_keys_question(self, user_entry, event):
        text = cleanText(user_entry)
        post_keys = textToKeys(text, event['lang'])
        print('text_to_keys_question', event['message'], user_entry, post_keys)
        if len(post_keys) > 0:
            response = await self.get_first_answer_text_to_question_keys(post_keys)
            print('response', response)
            if not response:
                questions = await self.get_all_validated_questions_keys()
                if questions.count() > 0:
                    closest = findClosestText(text, list(questions))
                    if not closest:
                        await self.bot_message(
                            "I am sorry, I don't have any information on: \"" + event["message"] + "\"",
                            event)
                        return True
                    else:
                        print(event['message'], user_entry, closest)
                        if closest["score"] >= 0.8:
                            response = await self.get_first_answer_text_to_question(closest["text"])
                            await self.bot_message(response, event)
                            return True
                        else:
                            # propose rephrase
                            question = await self.get_first_validated_question_for_keys(closest["text"])
                            if question:
                                msg = {
                                    "msg": "post.similar_question",
                                    "question": question,
                                    "user_question": user_entry,
                                    "send_back": {
                                        "yes": 'true',
                                        "no": 'true'
                                    },
                                    "post_id": event["post_id"]
                                }
                                await self.chat_bot_message({
                                    "message": msg,
                                    "room_id": event["room_id"]
                                })
                                return True
            
            if response:
                await self.bot_message(response, event)
                return True
