from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework import status
from accounts.models import get_user_from_token
from rest_framework.authentication import get_authorization_header
from django.http import JsonResponse
from chatrooms.models import Room
from chatrooms.serializers import RoomSerializer

# Create your views here.
@api_view(['GET'])
@csrf_exempt
def chatrooms_get(request, format='json'):
    user = get_user_from_token(get_authorization_header(request))
    if user:
        rooms = RoomSerializer(Room.objects.all(), many=True)
        """[
            {"id": 1,
             "label": "Jane Doe",
             "description": "I played the role of Georgia in Breaking Bad. I'm also known for playing "
                             "Malcom mother in Malcom in the Middle.",
             "portrait": "/static/img/profile/chatting_01_portrait.png",
             "image": "/static/img/profile/chatting_01.jpg"
             },
            {"id": 2,
             "label": "Clara Kent",
             "notepad": "I'm a fictional character first created for comic books by Jerry Siegel and "
                             "Joe Shuster in 1938 as the alternate identity of Superman cousine.",
             "portrait": "/static/img/profile/chatting_02_portrait.png",
             "image": "/static/img/profile/chatting_02.jpg"
             },
            {"id": 3,
             "label": "Bryan Cranston",
             "notepad": "I played the role of Walter in Breaking Bad. I'm also known for playing Hal in "
                             "Malcom in the Middle.",
             "portrait": "/static/img/profile/chatting_03_portrait.png",
             "image": "/static/img/profile/chatting_03.jpg"
             }
        ]"""
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
