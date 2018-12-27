from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework import status
from accounts.models import get_user_from_token
from rest_framework.authentication import get_authorization_header
from django.http import JsonResponse
from chatrooms.models import Room
from chatrooms.serializers import RoomSerializer, DataSerializer


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
        print(request.data)
        serializer = RoomSerializer(data=request.data)
        if serializer.is_valid(raise_exception=False):
            room = serializer.save()
            if room:
                rooms = RoomSerializer(Room.objects.all(), many=True)
                return JsonResponse({"chatrooms": rooms.data}, status=status.HTTP_200_OK)
            return JsonResponse({"message": "chatrooms.couldNotCreatedTheRoom"}, status=status.HTTP_201_CREATED)
        return JsonResponse({"message": "chatrooms.invalidRequestDataGiven"}, status=status.HTTP_200_OK)
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
        return JsonResponse({"message": "chatrooms.invalidRequestDataGiven"}, status=status.HTTP_200_OK)
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
