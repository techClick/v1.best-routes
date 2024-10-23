from get_routes.utils.coordinates import geocode
from .location import get_coords_from_location

def is_digit(param):
  return param.replace('.', '', 1).replace('-', '', 1).isdigit()

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
    return geocode(''.join([new_param, ', US']))

  return ''.join(new_param.split(' ')).split(',')