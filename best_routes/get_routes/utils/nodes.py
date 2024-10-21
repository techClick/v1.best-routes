import requests
import json

node_interval = 3

def get_nodes(source, destination):
  # This gets the nodes from openstreetmap, a node is an id for data of a geographic location
  # A node covers 0.1 miles in geography
  start = '{},{}'.format(source[0], source[1])
  end = '{},{}'.format(destination[0], destination[1])

  url = (
    'http://router.project-osrm.org/route/v1/driving/{};{}?alternatives=false&annotations=nodes'    
  ).format(start, end)
  headers = { 'Content-type': 'application/json'}

  print(url)
  try:
    r = requests.get(url, headers = headers)
    route_json = r.json()
    f = open('get_routes/check.json', 'w')
    f.write(json.dumps(route_json))
    f.close()
    print("Calling API ...:", r.status_code)

    if ('routes' in route_json):
      return {
        'geometry': route_json['routes'][0]['geometry'],
        'nodes': route_json['routes'][0]['legs'][0]['annotation']['nodes']
      }
  except:
    return None

  return None