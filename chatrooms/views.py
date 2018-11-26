from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework import status
from accounts.models import get_user_from_token
from rest_framework.authentication import get_authorization_header
from django.http import JsonResponse


# Create your views here.
@api_view(['GET'])
@csrf_exempt
def chatrooms_get(request, format='json'):
    user = get_user_from_token(get_authorization_header(request))
    if user:
        chatrooms = [
            {"id": 1,
             "user_label": "Bob Synclar",
             "user_notepad": "Bryan Cranston played the role of Walter in Breaking Bad. He is also known for playing Hal in Malcom in the Middle."
             },
            {"id": 2,
             "user_label": "Jone Doe",
             "user_notepad": "Jone Doe played the role of Walter in Breaking Bad. He is also known for playing Hal in Malcom in the Middle.",
             },
            {"id": 3,
             "user_label": "Clark Kent",
             "user_notepad": "Clark Kent is a fictional character first created for comic books by Jerry Siegel and Joe Shuster in 1938 as the alternate identity of Superman.",
             }
        ]
        return JsonResponse({"chatrooms": chatrooms}, status=status.HTTP_200_OK)
    return JsonResponse({"message": "user.nonConnected"}, status=status.HTTP_200_OK)
