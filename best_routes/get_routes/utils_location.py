from geopy.geocoders import Nominatim

def get_location_details(lonLat):
  geolocator = Nominatim(user_agent="myApp")
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