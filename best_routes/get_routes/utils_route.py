import requests
import json
import os
from .utils_nodes import get_nodes
from .utils_gas_stations import get_gas_stations


def get_coordinates(nodes):
  url = 'https://overpass-api.de/api/interpreter'
  route_nodes = None

  try:
    urlBody = 'data=\n[out: json]\n;\n(\n'

    def add_api_string(string, node):
      return string + 'node({});\n'.format(node)

    if (len(nodes) <= 3):
      for node_ in nodes:
        urlBody = add_api_string(urlBody, node)
    else:
      for i in range(0, len(nodes)):
        if (i % 3 == 1):
          urlBody = add_api_string(urlBody, nodes[i])

    urlBody = urlBody + ');\n(._;>;);\nout;'
    res = requests.post(url, urlBody)
    print("Calling API 2 ...:", res.status_code, res.json())
    result = res.json()

    if ('elements' in result):
      return result['elements']

    return None
  except:
    return None

def get_route(source, destination):
  if (not source or not destination):
    return { 'isError': 'Source or destination missing' }

  file = open('get_routes/mock_coordinates.json', 'r')
  coordinates_src = json.load(file)['elements']

  if (os.getenv('ENVIRONMENT') == 'production'):
    nodes = get_nodes(source, destination)
    coordinates_src = get_coordinates(nodes)

  if (not coordinates_src):
    return { 'isError': 'No route data found' }
  
  coordinates = []

  for entry in coordinates_src:
    coordinates.append([entry['lon'], entry['lat']])

  coordinates.sort(key=lambda coordinates: coordinates[0])
  gas_stations_obj = get_gas_stations(coordinates)

  if (not gas_stations_obj['gas_stations'] or len(gas_stations_obj['gas_stations']) == 0):
    return { 'isError': 'No gas stations found' }

  route = {
    'coordinates': coordinates,
    'gas_stations_obj': gas_stations_obj
  }
  
  return route