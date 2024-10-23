import os
from azure.core.exceptions import HttpResponseError # type: ignore
from azure.core.credentials import AzureKeyCredential # type: ignore
from azure.maps.search import MapsSearchClient # type: ignore
from azure.maps.route import MapsRouteClient # type: ignore

node_interval = 4
miles_per_coordinate = node_interval / 10

subscription_key = os.getenv('AZURE_SUBSCRIPTION_KEY')
credential=AzureKeyCredential(subscription_key)

def get_route_from_azure(source, destination):
  route_client = MapsRouteClient(credential=credential)
  route_directions_result = route_client.get_route_directions(route_points=[source, destination])
  route = [[coord.longitude, coord.latitude] for coord in route_directions_result.routes[0].legs[0].points]
  route = [coords for i, coords in enumerate(route) if i % node_interval == 1]
  meters = route_directions_result.routes[0].legs[0].summary.length_in_meters

  return route

def geocode(city):
  maps_search_client = MapsSearchClient(credential=credential)

  try:
    result = maps_search_client.get_geocoding(query=city)
    if result.get('features', False):
      coordinates = result['features'][0]['geometry']['coordinates']
      return [coordinates[0], coordinates[1]]
    else:
      return 'api error'

  except HttpResponseError as exception:
    return 'api error'