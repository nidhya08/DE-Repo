import csv
import pandas as pd
import requests
import json
import folium
import sys
from enum import Enum


# This program uses list of lat, lon in given CSV file, inputs these data points to HERE Map API to find
# best point sequence followed by best possible route to cover all locations
# This can be used by delivery persons to cover every delivery point in an efficient manner

class QueryParm(Enum):
    MODE = 'fastest;car'
    RPR = 'display'


# method to get the cluster input from csv file - then retrieve the co -ordinates
def fetchInfoFromCsv(cluster_csv):
    with open(cluster_csv) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        is_header = True
        co_ord_list = []
        for row in csv_reader:
            if is_header:
                # skip the header part in csv file
                is_header = False
            else:
                # get the car park name, lat, lon values resp.
                co_ord_list.append([row[5], row[6], row[7]])
    # convert the list to pandas DF
    co_ords = pd.DataFrame(co_ord_list, columns=['carpark', 'lat', 'lon'])
    return co_ords


# method to run the findsequence REST API and retrieve the order
def getOrderedCoord(app_id, app_code, co_ords):
    # HERE map api to find the best order among given waypoints, given the dest and end point
    formulate_url = 'https://wse.api.here.com/2/findsequence.json'
    count = 0
    dest_str = ''
    for row in co_ords.itertuples(index=False):
        if count == 0:
            # currently, destination/end is set as the first co-ord in the given file
            start = '' + row[0] + ';geo!' + row[1] + ',' + row[2]
            end = '{}end;geo!{},{}'.format(row[0], row[1], row[2])
            count += 1
        else:
            dest_str += 'destination{}={};geo!{},{}&'.format(count, row[0], row[1], row[2])
            count += 1

    dest_str = dest_str[:-1]

    # formulate the query param to call the REST API
    formulate_url += '?app_id={}&app_code={}&mode={}&start={}&{}&end={}'.format(app_id, app_code, QueryParm.MODE.value,
                                                                                start, dest_str, end)

    # GET request of above mentioned API is fired
    response = requests.get(formulate_url)
    # Response object gives us the sequence
    result_json = json.loads(response.text)
    # call calcRoute method to calculate the route
    calcRoute(app_id, app_code, result_json['results'][0]['waypoints'])


# method to execute calcRoute REST API
def calcRoute(app_id, app_code, sequence):
    waypoints = ''
    # HERE map API to calculate the best possible route between 2 given points
    form_calc_route_url = 'https://route.api.here.com/routing/7.2/calculateroute.json'

    num = 0
    co_ord_list = []
    # Just a random location to focus the map -to start with (need to replace it with proper co-ord to singapore)
    m = folium.Map(location=[1.3345385, 103.8709152], zoom_start=5)

    for co_ord in sequence:
        waypoints += 'waypoint{}=geo!{},{}&'.format(num, co_ord['lat'], co_ord['lng'])
        folium.Marker((co_ord['lat'], co_ord['lng']), icon=folium.Icon(icon_color='green')).add_to(m)
        num += 1
    waypoints = waypoints[:-1]
    form_calc_route_url += '?app_id={}&app_code={}&mode={}&{}&representation={}'.format(app_id, app_code,
                                                                                        QueryParm.MODE.value, waypoints,
                                                                                        QueryParm.RPR.value)

    response = requests.get(form_calc_route_url)
    # response gives the shape object and the route between all given co-ords
    result_json = json.loads(response.text)
    # extracting the shape object from the response
    shapes_co_ord = result_json['response']['route'][0]['shape']
    count = 0

    for co_ord in shapes_co_ord:
        lat = float(co_ord.split(',')[0])
        lng = float(co_ord.split(',')[1])
        co_ord_list.append((lat, lng))

    # Create polyLine from given co-ords and add this line layer to the map object
    folium.PolyLine(co_ord_list).add_to(m)
    # save the map
    m.save('map_route.html')
    print("Map file <<map_route.html>> was generated successfully!! Check it out!")


if __name__ == '__main__':
    cmd_param = sys.argv
    app_id = sys.argv[1]
    app_code = sys.argv[2]
    csv_file = sys.argv[3]
    co_ords = fetchInfoFromCsv(csv_file)
    getOrderedCoord(app_id, app_code, co_ords)
