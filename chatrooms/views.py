from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework import status
from accounts.models import get_user_from_token
from rest_framework.authentication import get_authorization_header
from django.http import JsonResponse
from chatrooms.apps import get_chatBot
import time
import random
import math


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


def compute_response_time(request, response):
    # response time depend on len of text and should be between approximately 2s and 1 min
    rqlen = len(request)
    rlen = len(response)
    rand = random.randrange(1, 3)
    randMax = random.randrange(50, 60)
    response_time = min(math.ceil(rand * (rlen + rqlen) / 6), randMax)
    
    return response_time


@api_view(['POST'])
@csrf_exempt
def chat_post(request, format='json'):
    start_time = time.time()
    text = request.data['text']
    user = get_user_from_token(get_authorization_header(request))
    if user:
        if not text:
            return JsonResponse({
                'text': [
                    'The attribute "text" is required.'
                ]
            }, status=400)
            
        PokerFaceBot = get_chatBot()
        response = PokerFaceBot.get_response({'text': text})
        response_data = response.serialize()
        response_time = compute_response_time(text, response_data['text'])
        now_time = time.time()
        spend_time = now_time - start_time
        print(start_time, now_time, response_time, spend_time, response_time - spend_time)
        
        if spend_time < response_time:
            time.sleep(response_time - spend_time)
        
        return JsonResponse(response_data, status=status.HTTP_200_OK)
    return JsonResponse({"message": "user.nonConnected"}, status=status.HTTP_200_OK)
