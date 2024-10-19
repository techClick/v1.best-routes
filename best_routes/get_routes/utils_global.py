from .utils_location import get_location_from_coords
import csv
from operator import itemgetter
import math


def get_gas_stations(coordinates):
  miles_per_gallon = 10# 10
  max_gallons_in_tank = 10 # 50
  litres_per_gallon = 3.785
  miles_per_litre = miles_per_gallon / litres_per_gallon
  max_miles_in_tank = miles_per_gallon * max_gallons_in_tank
  min_litres = 20
  current_litres_in_tank = 0
  miles_per_coordinate = 0.3
  gas_stations_raw = []
  gas_stations = []
  total_price = 0

  with open('get_routes/fuel-prices.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        gas_stations_raw.append(row)

  # remove csv header
  gas_stations_raw = gas_stations_raw[1:]

  def add_gas_station(coordinate):
    nonlocal miles_per_gallon
    nonlocal miles_per_litre
    nonlocal litres_per_gallon
    nonlocal max_gallons_in_tank
    nonlocal gas_stations
    nonlocal total_price
    nonlocal current_litres_in_tank
    nonlocal gas_stations_raw
    nonlocal miles_per_coordinate

    # max gallons in vehicle * litres per gallon 
    max_litres_in_tank = 50 * litres_per_gallon
    location = get_location_from_coords(coordinate)
  
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
          'coordinates': coordinate
        })
        total_price = total_price + (price * current_litres_to_buy)
        current_litres_in_tank = max_litres_in_tank - (miles_per_coordinate / miles_per_litre)
      else:
        current_litres_in_tank = current_litres_in_tank - (miles_per_coordinate / miles_per_litre)
    else:
      current_litres_in_tank = current_litres_in_tank - (miles_per_coordinate / miles_per_litre)
 
  add_gas_station(coordinates[0])
  coordinates = coordinates[1:]
  mileage_to_start_search = 70
  search_area = max_miles_in_tank - mileage_to_start_search
  start_i = mileage_to_start_search - 1
  print('START I', start_i, len(coordinates))

  while(start_i < len(coordinates)):
    end_i = (start_i + math.floor(search_area / miles_per_coordinate)) - 1
    print(end_i)
    if (end_i > len(coordinates)):
      print('0 HERE', end_i, len(coordinates))
      break

    cheapest_gas_stations = []

    for j in range(start_i, end_i):
      print(j)
      location = get_location_from_coords(coordinates[j])

      if (location):
        location_gas_stations = (list(filter(lambda station: (
          station[3].strip() in location['town'] and station[4].strip().lower() == location['state'].lower()
        ), gas_stations_raw)))

        if (len(location_gas_stations) > 0):
          cheapest_gas_stations.append({
            'info': sorted(location_gas_stations, key=itemgetter(6))[0],
            'index': j
          })

    cheapest_gas_station = 1#sorted(cheapest_gas_stations, key=itemgetter(''))
    # print('HERE', cheapest_gas_stations, cheapest_gas_station)
    start_i = len(coordinates)


  # print(len(coordinates), len(gas_stations), gas_stations, len(coordinates) * 0.3)

  gas_stations_object = {
    'gas_stations': gas_stations,
    'total_price': total_price
  }

  return gas_stations_object