from .utils_location import get_location_details
import csv
from operator import itemgetter

def get_gas_stations(coordinates):
  litres_per_gallon = 3.785
  # miles per gallon / liters per gallon
  miles_per_litre = 10 / litres_per_gallon
  miles_per_coordinate = 0.3
  fuel_min_limit = 20
  gas_stations = []
  current_litres_in_tank = 0
  # max gallons in vehicle * litres per gallon 
  max_litres_in_tank = 50 * litres_per_gallon
  total_price = 0

  for i in range(0, len(coordinates)):
    if (current_litres_in_tank <= fuel_min_limit):
      gas_stations_raw = []
      location = get_location_details(coordinates[i])

      with open('get_routes/fuel-prices.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            gas_stations_raw.append(row)
    
      if (location):
        # remove header
        gas_stations_raw = gas_stations_raw[1:]
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
          total_price = total_price + (price * current_litres_to_buy)
          current_litres_in_tank = max_litres_in_tank
        else:
          current_litres_in_tank = current_litres_in_tank - (miles_per_coordinate / miles_per_litre)
      else:
        current_litres_in_tank = current_litres_in_tank - (miles_per_coordinate / miles_per_litre)
    else:
      current_litres_in_tank = current_litres_in_tank - (miles_per_coordinate / miles_per_litre)

  # print(len(coordinates), len(gas_stations), gas_stations, len(coordinates) * 0.3)

  gas_stations_object = {
    'data': gas_stations,
    'total_price': total_price
  }

  return gas_stations_object