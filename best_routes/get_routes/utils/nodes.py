import requests
import json

node_interval = 3

def get_nodes(source, destination):
  # This gets the nodes from openstreetmap, a node is an id for data of a geographic location
  # A node covers 0.1 miles in geography
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