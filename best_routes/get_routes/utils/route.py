import json
import os

from get_routes.utils.coordinates import get_route_from_azure
from get_routes.utils.logistics import get_logistics

def get_route(source, destination):
  if (not source or not destination):
    return { 'isError': 'Source or destination error' }


  if (os.getenv('ENVIRONMENT') == 'production'):
    coordinates = get_route_from_azure([source[1], source[0]], [destination[1], destination[0]])
    file = open('get_routes/mock_nodes.json', 'w')
    file.write(json.dumps(coordinates))
    file.close()
  else:
    file = open('get_routes/mock_nodes.json', 'r')
    coordinates = json.load(file)
    file.close()

  if (not coordinates):
    return { 'isError': 'Max API tries exceeded, please try later' }

  route = {
    'coordinates': coordinates,
    'points': '',
    'logistics': get_logistics(sorted(coordinates)),
    'geometry': ''
  }

  return route

# get_route('test', 'test')