from .utils_location import get_coords_from_location

def is_digit(param):
  return param.replace('.', '', 1).replace('-', '', 1).isdigit()

def get_param_type(param):
  param_type = 'city'

  if (param.strip().split(',')[1]):
    param_split = param.strip().split(',')

    if (is_digit(param_split[0].strip()) and is_digit(param_split[1].strip()) and len(param_split) == 2):
      param_type = 'coord'
  
  return param_type

def format_param(param):
  new_param = param

  if (get_param_type(new_param) == 'city'):
    new_param = get_coords_from_location(new_param)
  
  return new_param