import csv
import math
import json
from azure.core.exceptions import HttpResponseError # type: ignore
from azure.core.credentials import AzureKeyCredential # type: ignore
from azure.maps.search import MapsSearchClient # type: ignore

gs_lo = []

from azure.core.exceptions import HttpResponseError # type: ignore

gas_stations_raw = []
with open('get_routes/fuel-prices copy.csv', newline='') as csvfile:
  print('a HERE')
  spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
  count = 0
  for row in spamreader:
    count = count + 1

    if (count > 1):
      gas_stations_raw.append(row)

def geocode_batch():
  fails = 0
  locations = []

  maps_search_client = MapsSearchClient(credential=AzureKeyCredential('API KEY'))
  ind = -1
  limit = math.floor(len(gas_stations_raw) / 100)

  try:
    for i in range(0, limit):
      start = i * 100
      new_gas_stations = gas_stations_raw[start:start + 100]

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
        #print(longitude, latitude)
        locations.append({ 'lngLat': [longitude, latitude], 'id': ind })
        print({ 'lngLat': [longitude, latitude], 'id': ind })
        print('{}/{}'.format(len(locations), len(gas_stations_raw)), '{} fails'.format(fails))

  except HttpResponseError as exception:
    if exception.error is not None:
        print(f"Error Code: {exception.error.code}")
        print(f"Message: {exception.error.message}")

  f = open('get_routes/fuel-prices.json', 'w')
  f.write(json.dumps(locations))
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
