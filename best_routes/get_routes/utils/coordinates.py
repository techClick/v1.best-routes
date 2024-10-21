import json
import os
import requests

node_interval = 3

def get_coordinates(source, destination):
  url = '{}{}'.format(os.getenv('API_URL'), (
    '/route?points={}%2C{}%7C{}%2C{}&routeType=car'.format(
      source[1], source[0], destination[1], destination[0]
    )
  ))
  headers = {
    'Content-type': 'application/json',
    'x-rapidapi-host': os.getenv('API_HOST'),
    'x-rapidapi-key': os.getenv('RAPID_API_KEY')
  }

  try:
    res = requests.get(url, headers = headers)
    print("Calling API ...:", res.status_code)
    coordinates_src = json.loads(res.text)

    coords = [
      [
        coord['coordinate'][1],
        coord['coordinate'][0],
        coord['distance_miles']
      ] for coord in coordinates_src['paths'][0]['instructions']
    ]

    coordinates = {
      'coords': coords,
      'points': coordinates_src['paths'][0]['points'],
    }

    return coordinates
  except Exception as error:
    print('Maptoolkit API Error', error)
    return {
      'coords': [],
      'points': []
    }