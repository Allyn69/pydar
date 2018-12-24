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
    fig, ax = plt.subplots(figsize=(12, 12),
                           subplot_kw=dict(projection=projection))
    gl = ax.gridlines(draw_labels=True)
    gl.xlabels_top = gl.ylabels_right = False
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
    return fig, ax

def update2(self):
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

def update(self):
    r = requests.get('http://public-api.adsbexchange.com/VirtualRadar/AircraftList.json?lat=50.100499598&lng=14.2698953&fDstL=0&fDstU=200', headers={'Connection':'close'})
    js_str=r.json()
    lat_list=[]
    long_list=[]
    op_list =[]
    #print(js_str)
    #print(js_str['lastDv'])
    if js_str['lastDv'] == str(-1):
        return track,
    for a in annotation_list:
        a.remove()
    annotation_list[:] = []
    fig.canvas.draw()
    for flight_data in js_str['acList']:
        lat=flight_data['Lat']
        lon=flight_data['Long']
        op=flight_data['Icao']
        lat_list.append(lat)
        long_list.append(lon)
        op_list.append(op)
        print((op, lon, lat))
        ano = ax.annotate(flight_data['Icao'],
                    xy=(flight_data['Long'],flight_data['Lat']))
        annotation_list.append(ano)
    track.set_data(long_list,lat_list)
    return track,

if __name__ == '__main__':
    print("loading")
    projection = ccrs.PlateCarree()
    annotation_list = []
    osm_tiles=OSM()
    #extent = [14.1698953, 14.3698953,50.000499598, 50.200499598 ]
    extent = [12.5, 17, 48.5, 51]
    #osm_tiles=GoogleTiles()
    fig, ax =  create_map(projection)
    ax.set_extent(extent, projection)
    ax.add_image(osm_tiles,7)
    ax.plot([14.255998976],[50.100499598], 'bo')
    track, = ax.plot([],[],'ro')
    anim = animation.FuncAnimation(fig,update,interval=2000, blit=False)
    plt.show()
