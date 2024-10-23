
import os
from azure.core.exceptions import HttpResponseError # type: ignore
from azure.core.credentials import AzureKeyCredential # type: ignore
from azure.maps.search import MapsSearchClient # type: ignore

def is_digit(param):
  return param.replace('.', '', 1).replace('-', '', 1).isdigit()

subscription_key = os.getenv('AZURE_SUBSCRIPTION_KEY')
maps_search_client = MapsSearchClient(credential=AzureKeyCredential(subscription_key))

def geocode(city):
  try:
    result = maps_search_client.get_geocoding(query=city)
    if result.get('features', False):
      coordinates = result['features'][0]['geometry']['coordinates']
      return [coordinates[0], coordinates[1]]
    else:
      return 'api error'

  except HttpResponseError as exception:
    return 'api error'