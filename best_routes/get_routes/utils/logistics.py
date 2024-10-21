import math
from operator import itemgetter
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
  miles_per_coordinate = node_interval / miles_per_gallon
  miles_in_tank = 0
  mileage_to_search_for_gas = 150
 
  search_limit = 0.05

  if (coordinates):
    for i in range(0, len(coordinates)):
      if (miles_in_tank <= mileage_to_search_for_gas):
        location_gas_stations = []
        for gas_station in gas_stations_raw:
          lng_calc = gas_station[len(gas_station) - 1][0] - coordinates[i][0]
          lat_calc = gas_station[len(gas_station) - 1][1] - coordinates[i][1]

          if (lng_calc < 0):
            lng_calc = lng_calc * -1
          if (lat_calc < 0):
            lat_calc = lat_calc * -1

          if (lat_calc <= search_limit and lng_calc <= search_limit):
            location_gas_stations.append(gas_station)

        if (len(location_gas_stations) > 0):
          cheapest_gas_station = sorted(location_gas_stations, key=itemgetter(len(location_gas_stations[0]) - 1))[0]
          price = float(cheapest_gas_station[len(cheapest_gas_station) - 2])

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
            'coordinates': cheapest_gas_station[len(cheapest_gas_station) - 1]
          })
          gas_stations_raw = [station for station in gas_stations_raw if (
            not (station[1] == cheapest_gas_station[1] and station[4] == cheapest_gas_station[4])
          )]
          total_price = total_price + (price * current_litres_to_buy)
          miles_in_tank = max_miles_of_vehicle
        else:
          miles_in_tank = miles_in_tank - miles_per_coordinate
      else:
        miles_in_tank = miles_in_tank - miles_per_coordinate

  logistics = {
    'gas_stations': gas_stations,
    'total_price': '${:,.2f}'.format(round(total_price, 2))
  }

  return logistics