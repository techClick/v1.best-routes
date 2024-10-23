from operator import itemgetter
import requests
import json
import os

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
    nodes_src = get_nodes(source, destination)
    nodes = None

    if (nodes_src):
      nodes = get_nodes_overpass(nodes_src['nodes'])

      file = open('get_routes/mock_nodes.json', 'w')
      file.write(json.dumps({ 'nodes': nodes, 'geometry': nodes_src['geometry'] }))
      file.close()
  else:
    file = open('get_routes/mock_nodes.json', 'r')
    nodes_src = json.load(file)
    file.close()
    nodes = nodes_src['nodes']

  if (not nodes):
    return { 'isError': 'Max API tries exceeded, please try later' }

  nodes_format = [[node['lon'], node['lat']] for node in nodes]
  coordinates = sorted(nodes_format, key=itemgetter(0))
  
  lng_sorted_0 = sorted(coordinates, key=lambda coord: float(coord[0]))
  lat_sorted_0 = sorted(coordinates, key=lambda coord: float(coord[1]))
  lng_sorted = sorted([lng_sorted_0[0][0], lng_sorted_0[len(lng_sorted_0) - 1][0]], key=lambda coord: coord)
  lat_sorted = sorted([lat_sorted_0[0][1], lat_sorted_0[len(lng_sorted_0) - 1][1]], key=lambda coord: coord)
  all_bounding_box = [[lng_sorted[0], lng_sorted[1]], [lat_sorted[0], lat_sorted[1]]]

  if (all_bounding_box[1][1] - all_bounding_box[1][0] > all_bounding_box[0][1] - all_bounding_box[0][0]):
    coordinates = sorted(nodes_format, key=itemgetter(1))

  route = {
    'coordinates': coordinates,
    'points': '',
    'logistics': get_logistics(sorted(coordinates)),
    'geometry': nodes_src['geometry']
  }

  return route

# get_route('test', 'test')