import requests

def get_nodes(source, destination):
  # Service - 'route', mode of transportation - 'driving', without alternatives
  url = 'http://router.project-osrm.org/route/v1/driving/{};{}?alternatives=false&annotations=nodes'.format(
    source, destination
  )
  headers = { 'Content-type': 'application/json'}

  try:
    r = requests.get(url, headers = headers)
    route_json = r.json()
    print("Calling API ...:", r.status_code)

    if ('routes' in route_json):
      return route_json['routes'][0]['legs'][0]['annotation']['nodes']
  except:
    return None

  return None

def get_coordinates(nodes):
  url = 'https://overpass-api.de/api/interpreter'

  route_nodes = None

  try:
    urlBody = 'data=\n[out: json]\n;\n(\n'

    for node in nodes:
      urlBody = urlBody + 'node({});\n'.format(node) 

    urlBody = urlBody + ');\n(._;>;);\nout;'
    res = requests.post(url, urlBody)
    # print(res.json())
    print("Calling API 2 ...:", res.status_code)
    result = res.json()

    if ('elements' in result):
      return result['elements']

    return None
  except:
    return None