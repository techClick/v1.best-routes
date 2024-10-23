from .location import get_coords_from_location
import os
from azure.core.exceptions import HttpResponseError # type: ignore
from azure.core.credentials import AzureKeyCredential # type: ignore
from azure.maps.search import MapsSearchClient # type: ignore

def is_digit(param):
  return param.replace('.', '', 1).replace('-', '', 1).isdigit()

subscription_key = os.getenv('AZURE_SUBSCRIPTION_KEY')

def geocode(city):
  maps_search_client = MapsSearchClient(credential=AzureKeyCredential(subscription_key))
  try:
    result = maps_search_client.get_geocoding(query=city)
    if result.get('features', False):
      coordinates = result['features'][0]['geometry']['coordinates']
      return [coordinates[0], coordinates[1]]
    else:
      return 'api error'

  except HttpResponseError as exception:
    return 'api error'

def get_param_type(param):
  param_type = 'city'

  if (param and len(param.strip().split(',')) == 2):
    param_split = param.strip().split(',')

    if (is_digit(param_split[0].strip()) and is_digit(param_split[1].strip())):
      param_type = 'coord'
  
  return param_type

def format_param(param):
  new_param = param

  if (not param):
    return None

  if (get_param_type(new_param) == 'city'):
    new_param = get_coords_from_location(new_param)

  return ''.join(new_param.split(' ')).split(',')