import json
import matplotlib.pyplot as plt
from matplotlib import animation
import cartopy.crs as ccrs
from cartopy.io.img_tiles import OSM, GoogleTiles
import requests
from cartopy.io import shapereader
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import sys
from geopy import Point
from geopy.distance import vincenty
import random
import numpy as np

#GPS COORDINATES OF A POINT WE WANT TO OBSERVE
DEFAULT_LATITUDE = 50.10049959
DEFAULT_LONGITUDE = 14.255998976

def create_map(projection):
    # create figure and ax with gridlines and formated axes
    fig, ax = plt.subplots(figsize=(10, 10),
                           subplot_kw=dict(projection=projection))
    gl = ax.gridlines(draw_labels=True)
    gl.xlabels_top = False
    gl.ylabels_right = False
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
    return fig, ax

def update_flights5(self, long, lat, dist, flight_list):
    print('---------------------')
    # Request fro AdsExchange API
    url = 'http://public-api.adsbexchange.com/VirtualRadar/AircraftList.json'
    payload = {'lat': lat, 'lng': long,'fDstL': 0, 'fDstU': dist}
    #r = requests.get('http://public-api.adsbexchange.com/VirtualRadar/AircraftList.json?lat={}&lng={}&fDstL=0&fDstU={}'.format(lat, long, distKm), headers={'Connection':'close'})
    r = requests.get(url, params=payload, headers={'Connection':'close'})
    js_str=r.json()
    #lat_list=[]
    #long_list=[]
    #print(js_str)
    # Chekc if call was correct
    if js_str['lastDv'] == str(-1):
        return track_flights, annotation_list

    # Clean annotation list
    for anot in annotation_list:
        anot.remove()
    annotation_list[:] = []
    fig.canvas.draw()
    # Get lat, long a name of all flights
    #print(js_str['stm'])
    for flight in js_str['acList']:
        if flight['Icao'] == '8960ED':
            print(flight['PosTime'])
        if not flight['Icao'] in flight_list:
            flight_list[flight['Icao']] = [[], [], [], []]
            flight_list[flight['Icao']][3].append(random.choice(['b', 'g', 'r', 'c', 'm', 'y', 'k']))
        latitude = flight['Lat']
        longitude = flight['Long']
        icao = flight['Icao']
        postime = flight['PosTime']
        if len(flight_list[flight['Icao']][2]) > 1 and flight['Icao'] == '4BD153':
            print(flight_list[flight['Icao']][0][-1] - latitude)
        if len(flight_list[flight['Icao']][2]) > 1 and int(flight_list[flight['Icao']][2][-1]) >= int(flight['PosTime']):
            latitude = flight_list[flight['Icao']][0][-1]
            longitude = flight_list[flight['Icao']][1][-1]
            postime = flight_list[flight['Icao']][2][-1]
        flight_list[flight['Icao']][0].append(latitude)
        flight_list[flight['Icao']][1].append(longitude)
        flight_list[flight['Icao']][2].append(postime)
        lat_list.append(flight_list[flight['Icao']][0][-1])
        long_list.append(flight_list[flight['Icao']][1][-1])
        color_list.append(str(flight_list[flight['Icao']][3][-1]))

        #long_list.append(longitude)
        #print((icao, longitude, latitude))
        anonnotation = ax.annotate(icao,
                    xy=(longitude,latitude), fontsize=8, fontweight='bold', size=7, color=str(flight_list[flight['Icao']][3][-1]))
        annotation_list.append(anonnotation)
    data = np.array([long_list,lat_list], dtype=object)
    data = np.transpose(data)
    track_flights.set_offsets(data)
    track_flights.set_facecolors(color_list)
    return track_flights,


def create_extent(long, lat, dist):
    # TODO: rewrite to a loop
    # Callculate gps coordinates for square around point of interest
    extent_north =  vincenty(kilometers=dist).destination(Point(lat, long), 0).format_decimal()
    extent_east = vincenty(kilometers=dist).destination(Point(lat, long), 90).format_decimal()
    extent_south = vincenty(kilometers=dist).destination(Point(lat, long), 180).format_decimal()
    extent_west =  vincenty(kilometers=dist).destination(Point(lat, long), 270).format_decimal()
    return [float(extent_west.split(',')[1]), float(extent_east.split(',')[1]), float(extent_south.split(',')[0]), float(extent_north.split(',')[0])]

if __name__ == '__main__':

    print("loading")
    distKm = 200
    # Check if point of interest was correctly given
    # If not take default (Letiste Vaclav Havel)
    if len(sys.argv) == 3:
        latitude = float(sys.argv[1])
        longitude = float(sys.argv[2])
    else:
        latitude = DEFAULT_LATITUDE
        longitude = DEFAULT_LONGITUDE
        print("Using default values. Your arguments are wrong")

    # Create projection and tiles. See cartopy pckg for more info
    projection = ccrs.PlateCarree()
    annotation_list = []
    osm_tiles=GoogleTiles()
    #osm_tiles=OSM()

    flight_list = {}
    lat_list=[]
    long_list=[]
    color_list = []

    extent = create_extent(longitude, latitude, distKm)
    fig, ax = create_map(projection)

    # Put together extented projection with ax
    ax.set_extent(extent, projection)
    ax.add_image(osm_tiles, 8, interpolation='spline36')
    #ax.plot([longitude], [latitude], 'bs')
    track_flights = ax.scatter([],[],marker='o',c=[], s=4)#, fillstyle='none')
    fig.suptitle('This is a somewhat long figure title', fontsize=16)

    # Update the plot every 2 seconds until close
    anim = animation.FuncAnimation(fig, update_flights5,fargs=[longitude, latitude,  distKm, flight_list], interval=2000, blit=False)
    plt.show()
