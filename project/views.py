from django.views.generic.base import TemplateView
import os
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.http import JsonResponse
from rest_framework.authtoken.models import Token


class HomePageView(TemplateView):
  template_name = 'project/index.html'
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['DJANGO_ENV'] = os.environ['DJANGO_ENV']
    return context

@api_view(['POST'])
@csrf_exempt
def check_token(request, format=None):
  testToken = Token.objects.filter(key=request.data['token']).exists()
  return JsonResponse({"status": testToken})
