from django.shortcuts import HttpResponse
from .utils import get_nodes
from rest_framework.decorators import api_view
import json

# Create your views here.
@api_view(['POST'])
def get_routes(request):
  # r = get_nodes((-80, 35), (-70, 40))
  body_unicode = request.body.decode('utf-8')
  body = json.loads(request.body)
  source, destination = body.values()

  # print(source, destination)

  if (not source or not destination):
    return HttpResponse('error')

  # nodes = get_nodes(source, destination)

  print(nodes)

  if (not nodes):
    return HttpResponse('error')
  else:
    return HttpResponse('works')
