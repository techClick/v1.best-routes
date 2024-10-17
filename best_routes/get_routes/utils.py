import requests

def get_nodes(source, destination):
  # Service - 'route', mode of transportation - 'driving', without alternatives
  url = 'http://router.project-osrm.org/route/v1/driving/{};{}?alternatives=false&annotations=nodes'.format(
    source, destination
  )

  print(url)

  headers = { 'Content-type': 'application/json'}
  route_nodes = None

  try:
    r = requests.get(url, headers = headers)
    route_json = r.json()
    print("Calling API ...:", r.status_code)

    if ('routes' in route_json):
      route_nodes = route_json['routes'][0]['legs'][0]['annotation']['nodes']
  except:
    return None

  return route_nodes

def get_coordinates(nodes):
  print('HEllo here')