import random
import argparse
import requests
import matplotlib.pyplot as plt
from matplotlib import animation
import cartopy.crs as ccrs
from cartopy.io.img_tiles import OSM, GoogleTiles
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
from geopy import Point
from geopy.distance import vincenty
import numpy as np

def create_map(long, lat, ext):
    # create figure and ax with gridlines and formated axes
    projection = ccrs.PlateCarree()
    tiles = GoogleTiles(style="street")
    # check if google tiles have fetched correctly
    # if note use OSM tiles
    if tiles is None:
        tiles = OSM()
    fig, ax = plt.subplots(figsize=(10, 10),
                           subplot_kw=dict(projection=projection))
    gl = ax.gridlines(draw_labels=True)
    gl.xlabels_top = False
    gl.ylabels_right = False
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER

    ax.set_extent(ext, projection)
    ax.add_image(tiles, 8, interpolation='spline36')
    ax.plot([long], [lat], 'bs')
    fig.suptitle('Live Flight Tracker', fontsize=16)
    track_flights = ax.scatter([], [], marker='o', c=[], s=8)
    return fig, ax, track_flights

def update_flights(self, long, lat, dist, flight_list, fig, ax, track_flights):
    print('---------------------')
    # Request fro AdsExchange API
    url = 'http://public-api.adsbexchange.com/VirtualRadar/AircraftList.json'
    payload = {'lat': lat, 'lng': long, 'fDstL': 0, 'fDstU': dist}
    r = requests.get(url, params=payload, headers={'Connection':'close'})
    js_str = r.json()
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

    # Get lat, long a name of all flights
    #print(js_str['stm'])
    for flight in js_str['acList']:
        if not flight['Icao'] in flight_list:
            flight_list[flight['Icao']] = {'lat':[], 'long':[], 'postime':[], 'color':[]}
            flight_list[flight['Icao']]['color'].append(random.choice(['b', 'g', 'r', 'c', 'm', 'y', 'k']))

        latitude = flight['Lat']
        longitude = flight['Long']
        icao = flight['Icao']
        postime = flight['PosTime']

        #if len(flight_list[flight['Icao']][2]) > 1 and flight['Icao'] == '4BD153':
            #print(flight_list[flight['Icao']][0][-1] - latitude)
        if (len(flight_list[icao]['postime']) > 1 and
                int(flight_list[icao]['postime'][-1]) >= int(postime)):
            latitude = flight_list[icao]['lat'][-1]
            longitude = flight_list[icao]['long'][-1]
            postime = flight_list[icao]['postime'][-1]

        flight_list[icao]['lat'].append(latitude)
        flight_list[icao]['long'].append(longitude)
        flight_list[icao]['postime'].append(postime)

        lat_list.append(flight_list[icao]['lat'][-1])
        long_list.append(flight_list[icao]['long'][-1])
        color_list.append(str(flight_list[icao]['color'][-1]))

        anonnotation = ax.annotate(icao, xy=(longitude, latitude), fontsize=8,
                                   fontweight='bold', size=7,
                                   color=str(flight_list[icao]['color'][-1]))
        annotation_list.append(anonnotation)

    data = np.array([long_list, lat_list], dtype=object)
    data = np.transpose(data)
    track_flights.set_offsets(data)
    track_flights.set_facecolors(color_list)
    return track_flights,

def create_extent(long, lat, dist):
    # Callculate gps coordinates for square around point of interest
    extent_north = vincenty(kilometers=dist).destination(Point(lat, long), 0).format_decimal()
    extent_east = vincenty(kilometers=dist).destination(Point(lat, long), 90).format_decimal()
    extent_south = vincenty(kilometers=dist).destination(Point(lat, long), 180).format_decimal()
    extent_west = vincenty(kilometers=dist).destination(Point(lat, long), 270).format_decimal()
    return [float(extent_west.split(',')[1]), float(extent_east.split(',')[1]),
            float(extent_south.split(',')[0]), float(extent_north.split(',')[0])]

if __name__ == '__main__':

    print("loading...")
    # Initialize the parser

    parser = argparse.ArgumentParser(description="Live Flight Tracker")
    parser.add_argument("longitude", type=float, help="Longitude of a observing point")
    parser.add_argument("latitude", type=float, help="Latitude of a observing point")
    parser.add_argument("-d", "--distance", type=int, default=200,
                        help="destination in km to cover from observing point")
    args = parser.parse_args()

    DISTKM = args.distance
    LATITUDE = args.latitude
    LONGITUDE = args.longitude

    print("Observing Long:{}, Lat:{} with range of {} km.".format(LONGITUDE, LATITUDE, DISTKM))

    EXTENT = create_extent(LONGITUDE, LATITUDE, DISTKM)
    figure, axes, track_flights = create_map(LONGITUDE, LATITUDE, EXTENT)

    # Create projection and tiles. See cartopy pckg for more info
    flight_list = {}
    lat_list = []
    long_list = []
    color_list = []
    annotation_list = []

    # Update the plot every 2 seconds until close
    anim = animation.FuncAnimation(figure, update_flights, fargs=[LONGITUDE, LATITUDE, DISTKM, flight_list, figure, axes, track_flights], interval=2000, blit=False)
    plt.show()
