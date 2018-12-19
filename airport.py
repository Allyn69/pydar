#%matplotlib tk
import json
import matplotlib.pyplot as plt
from matplotlib import animation
import cartopy.crs as ccrs
from cartopy.io.img_tiles import OSM, GoogleTiles
import requests
from cartopy.io import shapereader
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER


def create_map(projection):
    fig, ax = plt.subplots(figsize=(9, 13),
                           subplot_kw=dict(projection=projection))
    gl = ax.gridlines(draw_labels=True)
    gl.xlabels_top = gl.ylabels_right = False
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
    return fig, ax

def update(self):
    from opensky_api import OpenSkyApi
    api = OpenSkyApi()
    lat_list=[]
    long_list=[]
    # bbox = (min latitude, max latitude, min longitude, max longitude)
    states = api.get_states(bbox=(50.000499598, 50.200499598, 14.1698953, 14.3698953))
    for s in states.states:
        lat=s.latitude
        lon=s.longitude
        lat_list.append(lat)
        long_list.append(lon)
    print(long_list,lat_list)
    track.set_data(long_list,lat_list)
    return track,

def update1(self):
    #SEND QUERY
    r = requests.get('http://public-api.adsbexchange.com/VirtualRadar/AircraftList.json?lat=50.100499598&lng=14.2698953&fDstL=0&fDstU=20', headers={'Connection':'close'})
    js_str=r.json()
    lat_list=[]
    long_list=[]

    for num,flight_data in enumerate(js_str['acList']):
        lat=flight_data['Lat']
        lon=flight_data['Long']
        lat_list.append(lat)
        long_list.append(lon)
    print(long_list,lat_list)
    track.set_data(long_list,lat_list)
    return track,

if __name__ == '__main__':
    print("loading")
    projection = ccrs.PlateCarree()
    osm_tiles=OSM()
    extent = [14.1698953, 14.3698953,50.000499598, 50.200499598 ]
    #extent = [14.1, 14.4, 49.9, 50.4]
    #osm_tiles=GoogleTiles()
    fig, ax =  create_map(projection)
    ax.set_extent(extent, projection)

    ax.add_image(osm_tiles,13) #Zoom Level 13
    #PLOT JFK INTL AIRPORT
    ax.text(14.2698953,50.100499598,'letiště václava havla',horizontalalignment='right',size='large')
    ax.plot([14.255998976],[50.100499598], 'bo')
    #PLOT TRACK
    track,  = ax.plot([], [],'ro')
    anim = animation.FuncAnimation(fig, update1,interval=3000, blit=False)
    plt.show()
