import math
import json
from get_routes.utils.coordinates import miles_per_coordinate

def get_logistics(coordinates):
  file = open('get_routes/locations.json', 'r')
  gas_stations_raw = json.load(file)
  litres_per_gallon = 3.785
  miles_per_gallon = 10
  liters_per_mile = litres_per_gallon / miles_per_gallon
  max_gallons_in_vehicle = 50
  max_miles_of_vehicle = max_gallons_in_vehicle * miles_per_gallon
  max_litres_in_vehicle = max_gallons_in_vehicle * litres_per_gallon
  gas_stations = []
  total_price = 0
  miles_in_tank = 0
  mileage_to_search_for_gas = 350
  max_mileage_to_drive = max_miles_of_vehicle - mileage_to_search_for_gas
  coord_drive_range = math.ceil(max_mileage_to_drive / miles_per_coordinate)
  
  lng_sorted_0 = sorted(coordinates, key=lambda coord: float(coord[0]))
  lat_sorted_0 = sorted(coordinates, key=lambda coord: float(coord[1]))
  lng_sorted = sorted([lng_sorted_0[0][0], lng_sorted_0[len(lng_sorted_0) - 1][0]], key=lambda coord: coord)
  lat_sorted = sorted([lat_sorted_0[0][1], lat_sorted_0[len(lng_sorted_0) - 1][1]], key=lambda coord: coord)
  all_bounding_box = [[lng_sorted[0], lng_sorted[1]], [lat_sorted[0], lat_sorted[1]]]

  all_gas_stations = list(filter(lambda gas_station: (
    gas_station[7][0] <= all_bounding_box[0][1] and gas_station[7][0] >= all_bounding_box[0][0] and (
      gas_station[7][1] <= all_bounding_box[1][1] and gas_station[7][1] >= all_bounding_box[1][0]
    )
  ), gas_stations_raw))

  coordinates_travelled = 0

  def get_gas_station_coord(gas_station, coordinates):
    get_closest_coord = (
      lambda g_station,
      coordinates:min(coordinates,key=lambda x: abs(x[0] - g_station[7][0]) and abs(x[1] - g_station[7][1]))
    )
    closest_coord = get_closest_coord(gas_station,coordinates)
    index = len(coordinates)
    index = next(
      i for i, coord in enumerate(coordinates) if coord[0] == closest_coord[0] and coord[1] == closest_coord[1]
    )
    return [ closest_coord, index ]

  lines = []

  while (coordinates_travelled < len(coordinates)):
    coord_search_range = math.ceil(mileage_to_search_for_gas / miles_per_coordinate)
    if (coordinates_travelled == 0):
      coord_search_range = 10

    cheapest_gas_station = None
    this_coordinates = coordinates[coordinates_travelled:coordinates_travelled + coord_search_range]

    lng_sorted_0 = sorted(this_coordinates, key=lambda coord: float(coord[0]))
    lat_sorted_0 = sorted(this_coordinates, key=lambda coord: float(coord[1]))
    lng_sorted = sorted([lng_sorted_0[0][0], lng_sorted_0[len(lng_sorted_0) - 1][0]], key=lambda coord: coord)
    lat_sorted = sorted([lat_sorted_0[0][1], lat_sorted_0[len(lng_sorted_0) - 1][1]], key=lambda coord: coord)

    increment = 1 if coordinates_travelled == 0 else 0
    bounding_box = [
      [lng_sorted[0] - increment, lng_sorted[1] + increment],
      [lat_sorted[0] - increment, lat_sorted[1] + increment]
    ]

    gas_stations_nearby = list(filter(lambda gas_station: (
      gas_station[7][0] <= bounding_box[0][1] and gas_station[7][0] >= bounding_box[0][0] and (
        gas_station[7][1] <= bounding_box[1][1] and gas_station[7][1] >= bounding_box[1][0]
      )
    ), all_gas_stations))

    gas_station_coord_range = None

    if (len(gas_stations_nearby) > 0):
      cheapest_gas_station = sorted(gas_stations_nearby, key=lambda gas_station: float(gas_station[6]))[0]
      gas_station_coord_src = get_gas_station_coord(cheapest_gas_station, this_coordinates)
      gas_station_coord_index = gas_station_coord_src[1]
      gas_station_coord = gas_station_coord_src[0]
      coord_drive_range = math.ceil(max_mileage_to_drive / miles_per_coordinate)

      # development code
      # if (coordinates_travelled > 0):
      #   drive_coordinates = coordinates[coordinates_travelled:coordinates_travelled + gas_station_coord_index]
      #   lines.append({
      #     'type': 'LineString',
      #     'coordinates': drive_coordinates
      #   })

      price = float(cheapest_gas_station[6])
      gas_station_coord_range = gas_station_coord_index + coord_drive_range
      miles_in_tank = miles_in_tank - (gas_station_coord_range * miles_per_coordinate)
      current_litres_to_buy0 = (max_miles_of_vehicle - miles_in_tank) * liters_per_mile
      current_litres_to_buy = current_litres_to_buy0 if (current_litres_to_buy0 <= max_litres_in_vehicle) else (
        max_litres_in_vehicle
      )

      gas_stations.append({
        'info': {
          'name': cheapest_gas_station[1],
          'price': price * current_litres_to_buy,
          'gallons_bought': round(current_litres_to_buy / litres_per_gallon)
        },
        'coordinates': gas_station_coord
      })
      miles_in_tank = max_miles_of_vehicle
      total_price = total_price + (price * current_litres_to_buy)
      coordinates_travelled = coordinates_travelled + gas_station_coord_range
    else:
      coordinates_travelled = coordinates_travelled + coord_search_range
      miles_in_tank = miles_in_tank - (coord_search_range * miles_per_coordinate)

  logistics = {
    'gas_stations': gas_stations,
    'total_price': '${:,.2f}'.format(round(total_price, 2)),
    'search_lines': lines
  }

  return logistics