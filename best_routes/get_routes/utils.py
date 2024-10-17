import requests

def get_nodes(source_arr, destination_arr):
  start = "{},{}".format(source_arr[0], source_arr[1])
  end = "{},{}".format(destination_arr[0], destination_arr[1])

  # Service - 'route', mode of transportation - 'driving', without alternatives
  url = 'http://router.project-osrm.org/route/v1/driving/{};{}?alternatives=false&annotations=nodes'.format(start, end)


  headers = { 'Content-type': 'application/json'}
  r = requests.get(url, headers = headers)
  print("Calling API ...:", r.status_code)

  route_json = r.json()
  # print(route_json) # Status Code 200 is success
  route_nodes = None
  if ('routes' in route_json):
    route_nodes = route_json['routes'][0]['legs'][0]['annotation']['nodes']
  # print(route_nodes) # Status Code 200 is success
  return route_nodes