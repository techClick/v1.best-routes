from django.shortcuts import render, HttpResponse
from .utils import get_nodes, get_coordinates
from rest_framework.decorators import api_view
import json
import os

def get_coordinates_call(source, destination):
  if (not source or not destination):
    return { 'isError': 'Source or destination missing' }

  file = open('get_routes/mock_coordinates.json', 'r')
  coordinates_src = json.load(file)['elements']

  if (os.getenv('ENVIRONMENT') == 'production'):
    nodes = get_nodes(source, destination)
    coordinates_src = get_coordinates(nodes)

  if (not coordinates_src):
    return { 'isError': 'No route data found' }

  coordinates = { 'body': [] }

  for entry in coordinates_src:
    coordinates['body'].append([entry['lon'], entry['lat']])
  
  return coordinates

@api_view(['POST'])
def get_routes(request):
  body = json.loads(request.body)
  source, destination = body.values()
  coordinates_result = get_coordinates_call(source, destination)

  if (coordinates_result['isError']):
    return HttpResponse(coordinates_result['isError'])
  else:
    return HttpResponse('success')

@api_view(['GET'])
def get_map(request):
  # remember virtual environment
  # indicate http response status
  # better notification
  # javascript var to const
  # r = get_nodes((-80, 35), (-70, 40))
  source, destination = [request.GET.get('source'), request.GET.get('destination')]
  coordinates_result = get_coordinates_call(source, destination)

  if ('isError' in coordinates_result):
    return HttpResponse(coordinates_result['isError'])
  else:
    return render(request, 'map.html', coordinates_result)
