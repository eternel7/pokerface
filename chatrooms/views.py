from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework import status
from datetime import datetime, timedelta
from accounts.models import get_user_from_token
from rest_framework.authentication import get_authorization_header
from django.http import JsonResponse
from chatrooms.models import Room, Post, UserInRoom
from chatrooms.serializers import RoomSerializer, DataSerializer, PostSerializer, UserInRoomReadSerializer
from chatrooms.serializers import QuestionSerializer


def create_or_update_post(user, post_dict):
    post_data = dict(post_dict)
    if 'post_id' in post_data:
        # update of existing post
        # no update for some fields
        if 'room' in post_data:
            del post_data['room']
        if 'owner' in post_data:
            del post_data['owner']
        
        post = Post.objects.filter(id=post_data['post_id'])
        if post.count() == 1:
            post = post.first()
            post.body = post_data['message']
            post.last_editor = user
            for key in post_data.keys():
                try:
                    setattr(post, key, post_data[key])
                except AttributeError:
                    print('No attribute ' + key + ' on Post')
            post.save()
            return post
    else:
        data = {
            "body": post_data['message'],
            "owner": user.pk,
            "room": post_data['room']
        }
        serializer = PostSerializer(data=data)
        if serializer.is_valid(raise_exception=False):
            post = serializer.save()
            if post:
                return post
        return serializer.errors
    return False


# Create your views here.
@api_view(['GET'])
@csrf_exempt
def chatrooms_get(request, format='json'):
    user = get_user_from_token(get_authorization_header(request))
    if user:
        rooms = RoomSerializer(Room.objects.all(), many=True)
        return JsonResponse({"chatrooms": rooms.data}, status=status.HTTP_200_OK)
    return JsonResponse({"message": "user.nonConnected"}, status=status.HTTP_200_OK)


@api_view(['POST'])
@csrf_exempt
def chatroom_post(request, format='json'):
    user = get_user_from_token(get_authorization_header(request))
    if user:
        serializer = RoomSerializer(data=request.data)
        if serializer.is_valid(raise_exception=False):
            room = serializer.save()
            if room:
                rooms = RoomSerializer(Room.objects.all(), many=True)
                return JsonResponse({"chatrooms": rooms.data}, status=status.HTTP_200_OK)
            return JsonResponse({"message": "room.couldNotCreatedTheRoom"}, status=status.HTTP_201_CREATED)
        return JsonResponse({"message": "room.invalidRequestDataGiven", "errors": serializer.errors},
                            status=status.HTTP_200_OK)
    return JsonResponse({"message": "user.nonConnected"}, status=status.HTTP_200_OK)


@api_view(['POST'])
@csrf_exempt
def chatroom_addData(request, format='json'):
    user = get_user_from_token(get_authorization_header(request))
    if user:
        data = {
            "label": request.data['label'],
            "description": request.data['description'],
            "raw_data": request.data['raw_data'],
            "room": request.data['room'],
        }
        serializer = DataSerializer(data=data)
        if serializer.is_valid(raise_exception=False):
            data = serializer.save()
            if data:
                rooms = RoomSerializer(Room.objects.all(), many=True)
                return JsonResponse({"chatrooms": rooms.data}, status=status.HTTP_200_OK)
            return JsonResponse({"message": "chatrooms.couldNotAddDataToTheRoom"}, status=status.HTTP_201_CREATED)
        return JsonResponse({"message": "chatrooms.invalidRequestDataGiven", "errors": serializer.errors},
                            status=status.HTTP_200_OK)
    return JsonResponse({"message": "user.nonConnected"}, status=status.HTTP_200_OK)


@api_view(['PUT'])
@csrf_exempt
def chatroom_update(request, format='json'):
    user = get_user_from_token(get_authorization_header(request))
    
    if isinstance(user, str):
        return JsonResponse({"message": user}, status=status.HTTP_200_OK)
    
    if user:
        roomId = request.data['id']
        room = Room.objects.filter(id=roomId)
        if room.count() == 1:
            room = room.first()
            room.label = request.data['label']
            room.description = request.data['description']
            image = request.data['image']
            if image.startswith("data:image/"):
                room.image = image
            portrait = request.data['portrait']
            if portrait.startswith("data:image/"):
                room.portrait = portrait
            room.save()
            
            rooms = RoomSerializer(Room.objects.all(), many=True)
            return JsonResponse({"chatrooms": rooms.data}, status=status.HTTP_200_OK)
        return JsonResponse({"message": "room.room_not_found_for_update"}, status=status.HTTP_200_OK)
    return JsonResponse({"message": "Profile.unauthorized_access"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['DELETE'])
@csrf_exempt
def chatroom_delete(request, room_id):
    user = get_user_from_token(get_authorization_header(request))
    
    if isinstance(user, str):
        return JsonResponse({"message": user}, status=status.HTTP_200_OK)
    
    if user:
        if room_id is not None:
            room = Room.objects.filter(id=room_id)
            if room.count() == 1:
                room = room.first()
                room.delete()
                
                rooms = RoomSerializer(Room.objects.all(), many=True)
                return JsonResponse({"chatrooms": rooms.data}, status=status.HTTP_200_OK)
        return JsonResponse({"message": "room.room_not_found_before_removing"}, status=status.HTTP_200_OK)
    return JsonResponse({"message": "Profile.unauthorized_access"}, status=status.HTTP_401_UNAUTHORIZED)


def stored_questions(room_id):
    return QuestionSerializer(Post.objects.filter(room=room_id, type=1), many=True)


@api_view(['POST'])
@csrf_exempt
def chat_question(request, format='json'):
    user = get_user_from_token(get_authorization_header(request))
    if user:
        request.data['type'] = 1 if request.data['question'] else 2
        del request.data['question']
        post = create_or_update_post(user, request.data)
        if post.pk:
            questions = stored_questions(request.data['room'])
            return JsonResponse({"post": PostSerializer(post).data, "questions": questions.data},
                                status=status.HTTP_200_OK)
        return JsonResponse({"message": "chatrooms.invalidRequestDataGiven", "errors": post.errors},
                            status=status.HTTP_200_OK)
    return JsonResponse({"message": "user.nonConnected"}, status=status.HTTP_200_OK)


@api_view(['GET'])
@csrf_exempt
def chat_questions(request, room_id, format='json'):
    user = get_user_from_token(get_authorization_header(request))
    if user:
        if room_id:
            questions = stored_questions(room_id)
            return JsonResponse({"questions": questions.data}, status=status.HTTP_200_OK)
        return JsonResponse({"message": "chatroom.invalidRequestDataGiven"}, status=status.HTTP_200_OK)
    return JsonResponse({"message": "user.nonConnected"}, status=status.HTTP_200_OK)


@api_view(['POST'])
@csrf_exempt
def chat_updateAnswer(request, format='json'):
    user = get_user_from_token(get_authorization_header(request))
    if user:
        question = request.data['question']
        if question and 'id' in question:
            q = Post.objects.filter(id=question['id'])
            if q.count() == 1:
                question = q.first()
        else:
            return JsonResponse({"message": "chatroom.invalidRequestDataGiven"}, status=status.HTTP_200_OK)
        
        room_id = question.room.pk
        answer = request.data['answer']
        if answer:
            if 'id' in answer:
                a = Post.objects.filter(id=answer['id'])
                if a.count() == 1:
                    answer = a.first()
                    answer.last_editor = user
                    answer.type = 2
                    answer.answer_to = question
                    answer.room = question.room
                    answer.save()
            else:
                data = {
                    "body": answer['message'],
                    "last_editor": user.pk,
                    "owner": user.pk,
                    "room": room_id,
                    "type": 2,
                    "answer_to": question.id
                }
                serializer = PostSerializer(data=data)
                print("data back", data)
                if serializer.is_valid(raise_exception=True):
                    answer = serializer.save()
                    print("data saved", answer)
            
            # save link question to answer
            print("answer back", answer)
            if answer:
                question.answer = answer
                question.save()
            
            answer = {
                "id": answer.pk,
                "message": answer.body,
                "date": answer.created_at,
                "type": 2,
                "answer_to": answer.answer_to.pk
            }
            question = {
                "id": question.pk,
                "answer": question.answer.pk
            }
            questions = stored_questions(room_id)
            return JsonResponse({"question": question, "answer": answer, "questions": questions.data},
                                status=status.HTTP_200_OK)
        return JsonResponse({"message": "chatroom.invalidRequestDataGiven"}, status=status.HTTP_200_OK)
    return JsonResponse({"message": "user.nonConnected"}, status=status.HTTP_200_OK)


@api_view(['GET'])
@csrf_exempt
def chatroom_users(request, room_id, format='json'):
    user = get_user_from_token(get_authorization_header(request))
    if user:
        if room_id:
            time_threshold = datetime.now() - timedelta(hours=2)
            users_in_room = UserInRoomReadSerializer(
                UserInRoom.objects.filter(room=room_id, updated_at__gt=time_threshold), many=True)
            return JsonResponse({"users": users_in_room.data}, status=status.HTTP_200_OK)
        return JsonResponse({"message": "chatroom.invalidRequestDataGiven"}, status=status.HTTP_200_OK)
    return JsonResponse({"message": "user.nonConnected"}, status=status.HTTP_200_OK)
