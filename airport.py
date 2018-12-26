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

print(len(sys.argv))
if len(sys.argv) == 3:
    LATITUDE = float(sys.argv[1])
    LONGITUDE = float(sys.argv[2])
else:
    LATITUDE = 50.10049959
    LONGITUDE = 14.255998976
    print("Using default values. Your arguments are wrong")

#GPS COORDINATES OF A POINT WE WANT TO OBSERVE
#LATITUDE = 50.10049959
#LONGITUDE = 14.255998976

def create_map(projection):
    fig, ax = plt.subplots(figsize=(10, 10),
                           subplot_kw=dict(projection=projection))
    gl = ax.gridlines(draw_labels=True)
    gl.xlabels_top = False
    gl.ylabels_right = False
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
    return fig, ax

def update_flights(self):
    r = requests.get('http://public-api.adsbexchange.com/VirtualRadar/AircraftList.json?lat={}&lng={}&fDstL=0&fDstU=100'.format(LATITUDE, LONGITUDE), headers={'Connection':'close'})
    js_str=r.json()
    lat_list=[]
    long_list=[]
    #print(js_str)
    #print(js_str['lastDv'])
    if js_str['lastDv'] == str(-1):
        return track, annotation_list

    for anot in annotation_list:
        anot.remove()

    annotation_list[:] = []
    fig.canvas.draw()

    for flight_data in js_str['acList']:
        latitude = flight_data['Lat']
        longitude = flight_data['Long']
        icao= flight_data['Icao']
        lat_list.append(latitude)
        long_list.append(longitude)
        #print((icao, longitude, latitude))
        anonnotation = ax.annotate(icao,
                    xy=(longitude,latitude), fontsize=8, fontweight='bold')
        annotation_list.append(anonnotation)
    track.set_data(long_list,lat_list)
    return track,

if __name__ == '__main__':
    print("loading")
    projection = ccrs.PlateCarree()
    annotation_list = []
    #osm_tiles=OSM()
    #extent = [int(LONGITUDE)-1.5, int(LONGITUDE)+3, int(LATITUDE)-1.5, int(LATITUDE)+1]
    distKm = 200
    extent_north =  vincenty(kilometers=distKm).destination(Point(LATITUDE, LONGITUDE), 0).format_decimal()
    extent_east = vincenty(kilometers=distKm).destination(Point(LATITUDE, LONGITUDE), 90).format_decimal()
    extent_south = vincenty(kilometers=distKm).destination(Point(LATITUDE, LONGITUDE), 180).format_decimal()
    extent_west =  vincenty(kilometers=distKm).destination(Point(LATITUDE, LONGITUDE), 270).format_decimal()
    #extent = [int(LONGITUDE)-2, int(LONGITUDE)+2, int(LATITUDE)-2, int(LATITUDE)+2]
    print(type(extent_west))
    print(extent_north)
    print(extent_south)
    print(extent_east)
    print(extent_west)
    extent = [float(extent_west.split(',')[1]), float(extent_east.split(',')[1]), float(extent_south.split(',')[0]), float(extent_north.split(',')[0])]
    osm_tiles=GoogleTiles()
    fig, ax =  create_map(projection)
    ax.set_extent(extent, projection)
    ax.add_image(osm_tiles,7,interpolation='spline36')
    ax.plot([LONGITUDE],[LATITUDE], 'bs')
    ax.text(LONGITUDE, LATITUDE, r'an equation: $E=mc^2$', fontsize=15)
    track, = ax.plot([],[],'ro')#, fillstyle='none')
    fig.suptitle('This is a somewhat long figure title', fontsize=16)
    anim = animation.FuncAnimation(fig,update_flights,interval=2000, blit=False)
    plt.show()
