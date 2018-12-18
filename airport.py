#%matplotlib tk
import urllib.request
import json
import matplotlib.pyplot as plt
from matplotlib import animation
import cartopy.crs as ccrs
from cartopy.io.img_tiles import OSM
import requests

#SET AXES
fig, ax = plt.subplots()
ax=plt.axes(projection=ccrs.PlateCarree())
ax.set_ylim(50.000499598,50.200499598)
ax.set_xlim(14.1698953,14.3698953)
print("1")
#ADD OSM BASEMAP
osm_tiles=OSM()
ax.add_image(osm_tiles,16, interpolation='bilinear') #Zoom Level 13
print("2")
#PLOT JFK INTL AIRPORT
ax.text(50.100499598,14.2698953,'JFK Intl',horizontalalignment='right',size='large')
ax.plot([50.100499598],[14.255998976],'bo')
print("3")
#PLOT TRACK
track, = ax.plot([], [],'ro')
print("4")

print("5")
#UPDATE FUNCTION
def update(self):
    #SEND QUERY
    r = requests.get('http://public-api.adsbexchange.com/VirtualRadar/AircraftList.json?lat=50.08239246&lng=14.300847&fDstL=0&fDstU=30', headers={'Connection':'close'})
    print(r.url)
    js_str=r.json()
    lat_list=[]
    long_list=[]

    for flight_data in js_str['acList']:
        lat_list.append(flight_data['Lat'])
        long_list.append(flight_data['Long'])
    track.set_data(long_list,lat_list)
    print(long_list,lat_list)
    return track

#UPDATING EVERY SECOND
anim = animation.FuncAnimation(fig, update,interval=1000, blit=False)
print("6")
plt.show()
