from geopy.geocoders import Nominatim # type: ignore

geolocator = Nominatim(user_agent = 'get_routes')

def get_location_from_coords(lonLat):
  coordinates = "{}, {}".format(lonLat[1], lonLat[0])
  location = geolocator.reverse(coordinates)

  location_return = None

  if (location.raw and 'town' in location.raw['address']):
    address = location.raw['address']
    location_return = {
      'town': address['town'],
      'state': address['ISO3166-2-lvl4'].split('-')[1]
    }

  return location_return 

def get_coords_from_location(city):
  coords = geolocator.geocode(', '.join([city, 'US']))
  coords_return = None

  if (coords and coords.longitude):
    coords_return = '{},{}'.format(coords.longitude, coords.latitude)

  return coords_return 