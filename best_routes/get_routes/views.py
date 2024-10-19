from django.shortcuts import render, HttpResponse
from .utils_route import get_route
from rest_framework.decorators import api_view
import json
from .utils_params import format_param

@api_view(['POST'])
def get_routes(request):
  body = json.loads(request.body)
  source, destination = body.values()
  source = format_param(source)
  destination = format_param(destination)
  route = get_route(source, destination)

  if ('isError' in route):
    return HttpResponse(route['isError'], status = 400)
  else:
    return HttpResponse('success')

@api_view(['GET'])
def get_map(request):
  # style the gas station points
  # Test your distance and gas station positioning logic, enhance too
  # check linter
  source, destination = [request.GET.get('source'), request.GET.get('destination')]
  source = format_param(source)
  destination = format_param(destination)
  route = get_route(source, destination)

  if ('isError' in route):
    return HttpResponse(route['isError'], status = 400)
  else:
    return render(request, 'map.html', route)
