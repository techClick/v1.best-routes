import csv
import math
import time
from django.shortcuts import render, HttpResponse
from get_routes.utils.route import get_route
from rest_framework.decorators import api_view # type: ignore
import json
from get_routes.utils.params import format_param

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
    route['logistics'].pop('gas_stations', None)
    return HttpResponse(json.dumps(route['logistics']), status = 200)

@api_view(['GET'])
def get_map(request):
  source, destination = [request.GET.get('source'), request.GET.get('destination')]
  source = format_param(source)
  destination = format_param(destination)
  route = get_route(source, destination)

  if ('isError' in route):
    return HttpResponse(route['isError'], status = 400)
  else:
    return render(request, 'map.html', route)
