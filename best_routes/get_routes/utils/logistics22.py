import math
from operator import itemgetter
import json

def get_logistics(coordinates):
  file = open('get_routes/locations.json', 'r')
  gas_stations_raw = json.load(file)
  litres_per_gallon = 3.785
  miles_per_gallon = 10
  liters_per_mile = litres_per_gallon / miles_per_gallon
  max_gallons_in_vehicle = 50
  max_miles_of_vehicle = max_gallons_in_vehicle * miles_per_gallon
  gas_stations = []
  total_price = 0
  miles_per_coordinate = 24000
  old_miles_in_tank = 0
  miles_in_tank = 0
  mileage_to_search_for_gas = 150
  max_mileage = max_miles_of_vehicle - mileage_to_search_for_gas

  print(sum(x[2] for x in coordinates), 'TOTAL')
  # for x in coordinates:
  #   print(x[2], 'EACH')
 
  search_limit = 0.15

  def search_for_gas_stations(coordinates, i):
    nonlocal miles_in_tank
    nonlocal mileage_to_search_for_gas
    nonlocal gas_stations_raw
    nonlocal max_miles_of_vehicle
    nonlocal gas_stations
    nonlocal litres_per_gallon
    nonlocal gas_stations_raw
    nonlocal total_price
    nonlocal miles_per_coordinate
    nonlocal old_miles_in_tank
    max_litres_in_vehicle = max_gallons_in_vehicle * litres_per_gallon

    if (miles_in_tank <= mileage_to_search_for_gas):
      location_gas_stations = []
      for gas_station in gas_stations_raw:
        lng_calc = gas_station[len(gas_station) - 1][0] - coordinates[0]
        lat_calc = gas_station[len(gas_station) - 1][1] - coordinates[1]

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
        print(miles_in_tank, current_litres_to_buy, i, 'To buy')
        # print(cheapest_gas_station[len(cheapest_gas_station) - 1], 'CHEAP')
        gas_stations.append({
          'info': {
            'name': cheapest_gas_station[1],
            'price': price * current_litres_to_buy,
            'gallons_bought': round(current_litres_to_buy / litres_per_gallon)
          },
          'coordinates': cheapest_gas_station[len(cheapest_gas_station) - 1]
        })
        print(cheapest_gas_station[1], cheapest_gas_station[7], coordinates, miles_in_tank, i, "Found")
        gas_stations_raw = [station for station in gas_stations_raw if (
          not (station[1] == cheapest_gas_station[1] and station[4] == cheapest_gas_station[4])
        )]
        total_price = total_price + (price * current_litres_to_buy)
        # coordinates[i - 1][2] is in miles (distance traveled)
        old_miles_in_tank = miles_in_tank
        miles_in_tank = max_miles_of_vehicle - math.ceil(coordinates[2])
        print(old_miles_in_tank, miles_in_tank, i, "found TANK")
      else:
        # gas_stations.append({
        #   'info': {
        #     'name': 'EMPTY',
        #     'price': 20,
        #     'gallons_bought': 20
        #   },
        #   'coordinates': coordinates[:2]
        # })
        old_miles_in_tank = miles_in_tank
        miles_in_tank_0 = miles_in_tank - math.ceil(coordinates[2])
        miles_in_tank = miles_in_tank_0 # if miles_in_tank_0 < mileage_to_search_for_gas else mileage_to_search_for_gas
        print(miles_in_tank, i, 'NOT found')
    else:
      old_miles_in_tank = miles_in_tank
      miles_in_tank_0 = miles_in_tank - math.ceil(coordinates[2])
      miles_in_tank = miles_in_tank_0 # if miles_in_tank_0 > mileage_to_search_for_gas else mileage_to_search_for_gas
      print(old_miles_in_tank, miles_in_tank, coordinates[2], i,  'Has gas')
    # print(miles_in_tank, coordinates[:2], coordinates[2], "DIST")

  if (coordinates):
    for i in range(0, len(coordinates)):
      search_for_gas_stations(coordinates[i], i)
      if (miles_in_tank < 0):
        print("----", coordinates[i][2], old_miles_in_tank, miles_in_tank, (old_miles_in_tank - miles_in_tank), coordinates[i][2] - (old_miles_in_tank - miles_in_tank))
        deficit = coordinates[i][2]# - (old_miles_in_tank - miles_in_tank)
        fuel_up_range = math.ceil(deficit / max_mileage)
        # print(fuel_up_range, deficit, deficit / fuel_up_range, 'FUEL RANGE')

        for j in range(0, fuel_up_range):
          this_mileage = max_mileage if (j < fuel_up_range - 1) else max_mileage * ((deficit / max_mileage) % 1)
          this_mileage_calc = (this_mileage * (j + 1)) / 10000
          if (coordinates[i - 1][0] > coordinates[i][0]):
            # lng_coord_deficit_0 = (coordinates[i - 1][0] - coordinates[i][0])
            # lng_coord_deficit = lng_coord_deficit_0 * this_mileage_calc # (deficit / fuel_up_range)
            # new_longitude = coordinates[i - 1][0] - lng_coord_deficit
            new_longitude = coordinates[i - 1][0] - this_mileage_calc
          else:
            # lng_coord_deficit_0 = (coordinates[i][0] - coordinates[i - 1][0])
            # lng_coord_deficit = lng_coord_deficit_0  * this_mileage_calc# (deficit / fuel_up_range)
            # new_longitude = coordinates[i - 1][0] + lng_coord_deficit
            new_longitude = coordinates[i - 1][0] + this_mileage_calc
          
          if (coordinates[i - 1][1] > coordinates[i][1]):
            # lat_coord_deficit_0 = (coordinates[i - 1][1] - coordinates[i][1])
            # lat_coord_deficit = lat_coord_deficit_0 * this_mileage_calc# (deficit / fuel_up_range)
            # new_latitude = coordinates[i - 1][1] - lat_coord_deficit
            new_latitude = coordinates[i - 1][1] - this_mileage_calc
          else:
            # lat_coord_deficit_0 = (coordinates[i][1] - coordinates[i - 1][1])
            # lat_coord_deficit = lat_coord_deficit_0 * this_mileage_calc# (deficit / fuel_up_range)
            # new_latitude = coordinates[i - 1][1] + lat_coord_deficit
            new_latitude = coordinates[i - 1][1] + this_mileage_calc

          new_distance = this_mileage # new_distance_0 if new_distance_0 < this_mileage else this_mileage
          print(miles_in_tank, deficit, coordinates[i - 1][0], new_longitude, new_distance, i, 'NEW')
          new_coordinates = [new_longitude, new_latitude, new_distance]
          search_for_gas_stations(new_coordinates, -1)
          

  # print(len(coordinates), len(gas_stations), len(coordinates) * 0.3)

  logistics = {
    'gas_stations': gas_stations,
    'total_price': '${:,.2f}'.format(round(total_price, 2))
  }

  return logistics