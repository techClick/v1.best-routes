import requests
import json

node_interval = 3

def get_nodes(source, destination):
  # This gets the nodes from openstreetmap, a node is an id for data of a geographic location
  # A node covers 0.1 miles in geography
  # This file is not used, it turned out to be a slower API comapred to other options

  source = '{},{}'.format(source[0], source[1])
  destination = '{},{}'.format(destination[0], destination[1])

  url = (
    'http://router.project-osrm.org/route/v1/driving/{};{}?alternatives=false&annotations=nodes'    
  ).format(source, destination)
  headers = { 'Content-type': 'application/json'}

  try:
    r = requests.get(url, headers = headers)
    route_json = r.json()
    print("Calling API ...:", r.status_code)

    if ('routes' in route_json):
      return {
        'geometry': route_json['routes'][0]['geometry'],
        'nodes': route_json['routes'][0]['legs'][0]['annotation']['nodes']
      }
  except Exception as e:
    print(e)
    return None

  return None