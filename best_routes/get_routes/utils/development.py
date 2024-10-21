import csv
import math
import json
from azure.core.exceptions import HttpResponseError # type: ignore
from azure.core.credentials import AzureKeyCredential # type: ignore
from azure.maps.search import MapsSearchClient # type: ignore

gs_lo = []

from azure.core.exceptions import HttpResponseError # type: ignore

gas_stations_raw = []
with open('get_routes/fuel-prices.csv', newline='') as csvfile:
  spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
  count = 0
  for row in spamreader:
    count = count + 1

    if (count > 1):
      gas_stations_raw.append(row)

file = open('get_routes/locations.json', 'r')
gas_stations = json.load(file)
file.close()

def geocode_batch():
  fails = 0

  maps_search_client = MapsSearchClient(credential=AzureKeyCredential('3j2qL8rggPwuhEjdxMjtDpSEFKPbXnx53CKGc8tD3oLOXKhQvXtsJQQJ99AJACYeBjFZx3OZAAAgAZMP17cZ'))
  limit = math.ceil(len(gas_stations_raw) / 100)
  ind = (100 * (limit - 1)) - 1

  try:
    for i in range(0, limit):
      start = i * 100
      new_gas_stations = gas_stations_raw[start:start + 100]

      if (i < limit - 1):
        continue

      batch_items = [
        {
          'query': ', '.join([gas_station[2], gas_station[4], 'US'])
        } for gas_station in new_gas_stations
      ]
      result = maps_search_client.get_geocoding_batch({
        "batchItems": batch_items,
      },)

      if not result.get('batchItems', False):
        ind = ind + 99
        print("No batchItems in geocoding")
        return

      for item in result['batchItems']:
        ind = ind + 1
        if not item.get('features', False):
            fails = fails + 1
            print(f"No features in item: {item}")
            continue

        coordinates = item['features'][0]['geometry']['coordinates']
        longitude, latitude = coordinates
        this_gas_station = gas_stations_raw[ind]
        this_gas_station.append([longitude, latitude])
        gas_stations.append(this_gas_station)
        print({ 'lngLat': [longitude, latitude], 'id': ind })
        print('{}/{}'.format(ind, len(gas_stations_raw)), '{} fails'.format(fails))

  except HttpResponseError as exception:
    if exception.error is not None:
        print(f"Error Code: {exception.error.code}")
        print(f"Message: {exception.error.message}")

  f = open('get_routes/locations.json', 'w')
  f.write(json.dumps(gas_stations))
  f.close()

def transfer_stations():
  new_gas_stations = []
  ind = 0
  for station in gas_stations_raw:
    gs_loc = next((x['lngLat'] for x in gs_lo if int(x['id']) == ind), None)
    new_gas_stations.append(station)
    ind = ind + 1
    if (gs_loc):
      new_gas_stations[len(new_gas_stations) - 1].append(gs_loc)
  print(len(new_gas_stations))
  f = open('get_routes/locations.json', 'w')
  f.write(json.dumps(new_gas_stations))
  f.close()
