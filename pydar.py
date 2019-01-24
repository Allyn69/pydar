import random
import argparse
import requests
import matplotlib.pyplot as plt
from matplotlib import animation
import cartopy.crs as ccrs
from cartopy.io.img_tiles import OSM, GoogleTiles, Stamen
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
from geopy import Point
from geopy.distance import vincenty
import numpy as np
import random
import cartopy.feature as cpf
from pydar.pydar import create_map, update_flights, create_extent, parse_args

if __name__ == '__main__':

    print("loading...")
    # Take input arguments
    DISTKM, LATITUDE, LONGITUDE = parse_args()

    print("Observing Long:{}, Lat:{} with range of {} km.".format(LONGITUDE, LATITUDE, DISTKM))
    # Compute coordinates of extended area
    EXTENT = create_extent(LONGITUDE, LATITUDE, DISTKM)
    figure, axes, track_flights = create_map(LONGITUDE, LATITUDE, EXTENT)

    # Create empty global variables for update_flights function
    flight_list = {}
    coords_list = []
    color_list = []
    annotation_list = []

    # Update the plot every 2 seconds until close
    #TODO: use blit to speed up
    anim = animation.FuncAnimation(figure, update_flights, fargs=[LONGITUDE, LATITUDE, DISTKM, flight_list, figure, axes, track_flights],
                                   interval=2000, blit=False)
    # Incase of missing tiles try to fetch them again
    try:
        plt.show()
    except ValueError:
        tiles = OSM()
        plt.show()
