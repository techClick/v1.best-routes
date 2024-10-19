from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent = 'get_routes')

def get_location_from_coords(lonLat):
  coordinates = "{}, {}".format(lonLat[1], lonLat[0])
  location = geolocator.reverse(coordinates)
  location_return = None

  if (location.raw):
    address = location.raw['address']
    location_return = {
      'town': address['town'],
      'state': address['ISO3166-2-lvl4'].split('-')[1]
    }

  return location_return 

def get_coords_from_location(city):
  location = geolocator.geocode(city)
  location_return = None

  print(location)
  if (location and location.longitude):
    location_return = ','.join([location.longitude, location.latitude])

  return location_return 