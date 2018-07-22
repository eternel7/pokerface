from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.http import JsonResponse
from rest_framework.authtoken.models import Token

@api_view(['POST'])
@csrf_exempt
def check_token(request, format=None):
  testToken = Token.objects.filter(key=request.data['token']).exists()
  return JsonResponse({"status": testToken})
