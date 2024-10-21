from django.shortcuts import render, HttpResponse
from get_routes.utils.route import get_route
import json
from get_routes.utils.params import format_param
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def get_routes(request):
  if (request.method == 'POST'):
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

@csrf_exempt
def get_map(request):
  if (request.method == 'GET'):
    source, destination = [request.GET.get('source'), request.GET.get('destination')]
    source = format_param(source)
    destination = format_param(destination)
    route = get_route(source, destination)

    if ('isError' in route):
      return HttpResponse(route['isError'], status = 400)
    else:
      return render(request, 'map.html', route)
