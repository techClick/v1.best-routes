from django.shortcuts import render, HttpResponse
from .utils import get_nodes, get_coordinates
from rest_framework.decorators import api_view
import json
import os

# Create your views here.
@api_view(['POST'])
def get_routes(request):
  # r = get_nodes((-80, 35), (-70, 40))
  body = json.loads(request.body)
  source, destination = body.values()

  if (not source or not destination):
    return HttpResponse('error')

  file = open('get_routes/mock_coordinates.json', 'r')
  coordinates_src = json.load(file)['elements']
  
  if (os.getenv == 'production'):
    nodes = get_nodes(source, destination)
    coordinates_src = get_coordinates(nodes)

  # remember virtual environment
  print(coordinates_src)

  if (not coordinates_src):
    return HttpResponse('error')
  else:
    return render(request, 'map.html')
    # return HttpResponse('works')
