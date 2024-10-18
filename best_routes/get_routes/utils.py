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
    # print(route_json)
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

    def add_api_string(string, node):
      return string + 'node({});\n'.format(node)

    if (len(nodes) <= 200):
      for node_ in nodes:
        urlBody = add_api_string(urlBody, node)
    else:
      for i in range(0, len(nodes)):
        if (i % 3 == 1):
          urlBody = add_api_string(urlBody, nodes[i])

    urlBody = urlBody + ');\n(._;>;);\nout;'
    res = requests.post(url, urlBody)
    print("Calling API 2 ...:", res.status_code)
    result = res.json()

    if ('elements' in result):
      return result['elements']

    return None
  except:
    return None