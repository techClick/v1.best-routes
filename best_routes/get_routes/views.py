from django.shortcuts import render, HttpResponse
from .utils import get_nodes, get_coordinates, get_route
from rest_framework.decorators import api_view
import json
import os

@api_view(['POST'])
def get_routes(request):
  body = json.loads(request.body)
  source, destination = body.values()
  route = get_route(source, destination)

  if (route['isError']):
    return HttpResponse(route['isError'])
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
  route = get_route(source, destination)

  if ('isError' in route):
    return HttpResponse(route['isError'])
  else:
    return render(request, 'map.html', route)
