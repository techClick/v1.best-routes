from .utils_location import get_location_from_coords
from .utils_nodes import node_interval
import csv
from operator import itemgetter

def get_logistics(coordinates):
  litres_per_gallon = 3.785
  miles_per_gallon = 10
  miles_per_litre = miles_per_gallon / litres_per_gallon
  # A node covers 0.1 miles in geography
  miles_per_coordinate = node_interval * 0.1
  min_litres = 20
  current_litres_in_tank = 0
  max_gallons_in_vehicle = 50
  max_litres_in_tank = max_gallons_in_vehicle * litres_per_gallon
  gas_stations = []
  total_price = 0
  location_fail_index = -1
  location_fail_range = ((max_gallons_in_vehicle * miles_per_gallon) / miles_per_coordinate) / 5
  location_fail_index = -1
  gas_stations_raw = []


  with open('get_routes/fuel-prices.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        gas_stations_raw.append(row)

  # remove csv header
  gas_stations_raw = gas_stations_raw[1:]

  for i in range(0, len(coordinates)):
    is_no_location_error = (
      location_fail_index == -1 or i - location_fail_index > location_fail_range
    )

    if (current_litres_in_tank <= min_litres and is_no_location_error):
      location = get_location_from_coords(coordinates[i])
      location_fail_index = -1
    
      if (location):
        location_gas_stations = list(filter(lambda station: (
          station[3].strip() in location['town'] and station[4].strip().lower() == location['state'].lower()
        ), gas_stations_raw))

        if (len(location_gas_stations) > 0):
          cheapest_gas_station = sorted(location_gas_stations, key=itemgetter(len(location_gas_stations[0]) - 1))[0]
          price = float(cheapest_gas_station[len(cheapest_gas_station) - 1])

          current_litres_to_buy0 = max_litres_in_tank - current_litres_in_tank
          current_litres_to_buy = current_litres_to_buy0 if (current_litres_to_buy0 <= 500) else 500
          gas_stations.append({
            'info': {
              'name': cheapest_gas_station[1],
              'price': price * current_litres_to_buy,
              'gallons_bought': current_litres_to_buy / litres_per_gallon
            },
            'coordinates': coordinates[i]
          })
          gas_stations_raw = [station for station in gas_stations_raw if not (
            not (station[1] == cheapest_gas_station[1] and station[4] == cheapest_gas_station[4])
          )]
          total_price = total_price + (price * current_litres_to_buy)
          current_litres_in_tank = max_litres_in_tank
        else:
          location_fail_index = i
          current_litres_in_tank = current_litres_in_tank - (miles_per_coordinate / miles_per_litre)
      else:
        location_fail_index = i
        current_litres_in_tank = current_litres_in_tank - (miles_per_coordinate / miles_per_litre)
    else:
      current_litres_in_tank = current_litres_in_tank - (miles_per_coordinate / miles_per_litre)

  # print(len(coordinates), len(gas_stations), gas_stations, len(coordinates) * 0.3)

  logistics = {
    'gas_stations': gas_stations,
    'total_price': total_price
  }

  return logistics