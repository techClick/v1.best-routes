from operator import itemgetter
import requests
import json
import os

from get_routes.utils.coordinates import get_route_from_azure
from get_routes.utils.nodes import get_nodes, node_interval
from get_routes.utils.logistics import get_logistics

def get_nodes_overpass(nodes):
  # This api converts all nodes to lng lat
  url = 'https://overpass-api.de/api/interpreter'

  try:
    urlBody = 'data=\n[out: json]\n;\n(\n'

    def add_api_string(string, node):
      return string + 'node({});\n'.format(node)

    if (len(nodes) <= node_interval):
      for node_ in nodes:
        urlBody = add_api_string(urlBody, node_)
    else:
      for i in range(0, len(nodes)):
        if (i % node_interval == 1):
          urlBody = add_api_string(urlBody, nodes[i])

    urlBody = urlBody + ');\n(._;>;);\nout;'
    res = requests.post(url, urlBody)
    print("Calling API Overpass ...:", res.status_code)
    result = res.json()

    if ('elements' in result):
      return result['elements']

    return None
  except:
    return None

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