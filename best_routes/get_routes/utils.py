import requests
import json
import os

def get_nodes(source, destination):
  # Service - 'route', mode of transportation - 'driving', without alternatives
  url = 'http://router.project-osrm.org/route/v1/driving/{};{}?alternatives=false&annotations=nodes'.format(
    source, destination
  )
  headers = { 'Content-type': 'application/json'}

  try:
    r = requests.get(url, headers = headers)
    route_json = r.json()
    # print(route_json)
    print("Calling API ...:", r.status_code)

    if ('routes' in route_json):
      return route_json['routes'][0]['legs'][0]['annotation']['nodes']
  except:
    return None

  return None

def get_fuelup_points(coordinates):
  gallonDistance = 10
  # max * liters in a gallon
  miles_per_litre = 10 / 3.785
  miles_per_node = 0.3
  fuel_min_limit = 150
  points = []
  current_fuel_in_tank = 0
  max_fuel_in_tank = 500

  for i in range(0, len(coordinates)):
    if (current_fuel_in_tank <= fuel_min_limit):
      points.append({
        'coordinates': coordinates[i]
      })
      current_fuel_in_tank = max_fuel_in_tank
    else:
      current_fuel_in_tank = current_fuel_in_tank - (miles_per_node * miles_per_litre)

  # print(len(coordinates), len(points), points, len(coordinates) * 0.3)
  return points


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
  context = {
    'coordinates': coordinates,
    'fuelup_points': get_fuelup_points(coordinates)
  }
  
  return context