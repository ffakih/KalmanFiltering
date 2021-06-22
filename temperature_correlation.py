#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 10 10:36:06 2021

@author: firasfakih
"""
import sys 
import pandas as pd
import numpy as np
from math import pi
import matplotlib.pyplot as plt

stations = pd.read_json(sys.argv[1], lines=True)
stations['avg_tmax'] = stations['avg_tmax'] / 10 #average daily high temp

city = pd.read_csv(sys.argv[2]).dropna()
city['area'] = city['area'] * 0.000001 #km^2
city = city[(city['area'] < 10000)]
city['pop_density'] = city['population'] / city['area']
city = city.reset_index(drop=True)



 # Haversine algorithm implementation for distance retrieved from: https://stackoverflow.com/questions/27928/calculate-distance-between-two-latitude-longitude-points-haversine-formula
 # Used from exercise 3
def distance(data,data2):
    p = pi/180
    R = 6371
    lat1,lon1 = data['latitude'] * p , data['longitude'] * p
    lat2, lon2 = data2['latitude'] * p , data2['longitude'] * p
    a = 0.5 - np.cos((lat2 - lat1))/2 + np.cos(lat1) * np.cos(lat2) * (1 - np.cos(lon2 - lon1))/2
    distance = 2 * R * np.arcsin(np.sqrt(a)) * 1000 # Metres
    return distance   

def best_tmax(city, stations):
    stations['distance'] = distance(city, stations)
    minimum_distance = stations['distance'].idxmin()
    return stations.loc[minimum_distance, 'avg_tmax']

city['avg_tmax'] = city.apply(best_tmax, stations=stations, axis=1)


plt.plot(city['avg_tmax'], city['pop_density'], 'r.')
plt.title("Temperature vs Population Density")
plt.xlabel('Avg Max Temperature (\u00b0C)')
plt.ylabel('Population Density (people/km\u00b2)')
plt.savefig(sys.argv[3])