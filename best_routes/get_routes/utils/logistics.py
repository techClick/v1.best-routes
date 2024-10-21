import math
import json
from get_routes.utils.nodes import node_interval

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
  miles_per_coordinate = node_interval / 10
  miles_in_tank = 0
  mileage_to_search_for_gas = 150
  max_mileage_to_drive = max_miles_of_vehicle - mileage_to_search_for_gas
 
  coord_search_range = 0.25
  
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

  def get_is_gas_station_coord(gas_station, coordinate):
    # print('COORD', gas_station[7], coordinate)
    search_range = 0.25
    lng_calc = gas_station[7][0] - coordinate[0]
    lat_calc = gas_station[7][1] - coordinate[1]

    if (lng_calc < 0):
      lng_calc = lng_calc * -1
    if (lat_calc < 0):
      lat_calc = lat_calc * -1

    return lat_calc <= search_range and lng_calc <= search_range

  while (coordinates_travelled < len(coordinates)):
    cheapest_gas_station = None
    coord_search_range = math.ceil(mileage_to_search_for_gas / miles_per_coordinate)
    this_coordinates = coordinates[coordinates_travelled:coordinates_travelled + coord_search_range]

    lng_sorted_0 = sorted(this_coordinates, key=lambda coord: float(coord[0]))
    lat_sorted_0 = sorted(this_coordinates, key=lambda coord: float(coord[1]))
    lng_sorted = sorted([lng_sorted_0[0][0], lng_sorted_0[len(lng_sorted_0) - 1][0]], key=lambda coord: coord)
    lat_sorted = sorted([lat_sorted_0[0][1], lat_sorted_0[len(lng_sorted_0) - 1][1]], key=lambda coord: coord)
    bounding_box = [[lng_sorted[0], lng_sorted[1]], [lat_sorted[0], lat_sorted[1]]]

    gas_stations_nearby = list(filter(lambda gas_station: (
      gas_station[7][0] <= bounding_box[0][1] and gas_station[7][0] >= bounding_box[0][0] and (
        gas_station[7][1] <= bounding_box[1][1] and gas_station[7][1] >= bounding_box[1][0]
      )
    ), all_gas_stations))

    gas_station_coord_range = None

    if (len(gas_stations_nearby) > 0):
      cheapest_gas_station = sorted(gas_stations_nearby, key=lambda gas_station: float(gas_station[6]))[0]

      try:
        gas_station_coord_index = next(
          i for i, v in enumerate(this_coordinates) if get_is_gas_station_coord(cheapest_gas_station, v)
        )
        coord_drive_range = math.ceil(max_mileage_to_drive / miles_per_coordinate)
        gas_station_coord_range = gas_station_coord_index + coord_drive_range
        price = float(cheapest_gas_station[6])
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
          'coordinates': cheapest_gas_station[7]
        })
        print('LITRES', current_litres_to_buy, miles_in_tank)
      except Exception as e:
        print('EXCEPT', e)
        gas_station_coord_range = coord_drive_range

    if (gas_station_coord_range):
      coordinates_travelled = coordinates_travelled + gas_station_coord_range
      miles_in_tank = max_miles_of_vehicle - (gas_station_coord_range * miles_per_coordinate)
    else:
      coordinates_travelled = coordinates_travelled + coord_search_range
      miles_in_tank = max_miles_of_vehicle - (coord_search_range * miles_per_coordinate)
    print(miles_in_tank, coordinates_travelled, gas_station_coord_range)

  logistics = {
    'gas_stations': gas_stations,
    'total_price': '${:,.2f}'.format(round(total_price, 2))
  }

  return logistics