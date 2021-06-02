#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 28 08:39:55 2021

@author: firasfakih
"""
import sys
import pandas as pd
import xml.dom.minidom as xml
from math import pi
import numpy as np
from pykalman import KalmanFilter

def get_data(file):
    parsed_data = xml.parse(file)
    trkpt = parsed_data.getElementsByTagName('trkpt')
    data = []
    for coords in trkpt:
        
        data.append({ 'lat': coords.getAttribute('lat') , 'lon':coords.getAttribute('lon')} ) 
    df_coords = pd.DataFrame(data,columns=['lat','lon'])
    df_coords = df_coords.apply(pd.to_numeric)
    return (df_coords)


''' 
    The Function below calculates the difference between latitude and logtitude using the Harvestine Formula
    The mathematics used was inspired by code found here : https://stackoverflow.com/questions/27928/calculate-distance-between-two-latitude-longitude-points-haversine-formula/21623206 
'''
def distance(data):
    p = pi/180
    R = 6371
    lat1,lon1 = data['lat'] * p , data['lon'] * p
    lat2, lon2 = data['lat'].shift(periods = -1, fill_value = 0) * p , data['lon'].shift(periods = -1, fill_value = 0) * p
    a = 0.5 - np.cos((lat2 - lat1))/2 + np.cos(lat1) * np.cos(lat2) * (1 - np.cos(lon2 - lon1))/2
    distance = 2 * R * np.arcsin(np.sqrt(a)) * 1000 # Metres
    distance = (distance.shift(periods=1, fill_value=0)).sum()
    return distance    


# kalman filtering
def smooth(data):
    initial_state = data.iloc[0]
    observation_covariance = np.diag([20, 20]) ** 2
    transition_covariance = np.diag([10,10]) ** 2 
    transition = [[1,0],[0,1]] 
    
    kf = KalmanFilter(initial_state_mean=initial_state,
        initial_state_covariance=observation_covariance,
        observation_covariance=observation_covariance,
        transition_covariance=transition_covariance,
        transition_matrices=transition
    )
    kalman_smoothed, _ = kf.smooth(data)
    kalman_smoothed = pd.DataFrame({'lat': kalman_smoothed[:, 0], 'lon': kalman_smoothed[:, 1]})
    return(kalman_smoothed)


def output_gpx(points, output_filename):
    """
    Output a GPX file with latitude and longitude from the points DataFrame.
    """
    from xml.dom.minidom import getDOMImplementation
    def append_trkpt(pt, trkseg, doc):
        trkpt = doc.createElement('trkpt')
        trkpt.setAttribute('lat', '%.8f' % (pt['lat']))
        trkpt.setAttribute('lon', '%.8f' % (pt['lon']))
        trkseg.appendChild(trkpt)
    
    doc = getDOMImplementation().createDocument(None, 'gpx', None)
    trk = doc.createElement('trk')
    doc.documentElement.appendChild(trk)
    trkseg = doc.createElement('trkseg')
    trk.appendChild(trkseg)
    
    points.apply(append_trkpt, axis=1, trkseg=trkseg, doc=doc)
    
    with open(output_filename, 'w') as fh:
        doc.writexml(fh, indent=' ')

def main():
    points = get_data(sys.argv[1])
    print('Unfiltered distance: %0.2f' % (distance(points),))
    
    smoothed_points = smooth(points)
    print('Filtered distance: %0.2f' % (distance(smoothed_points),))
    output_gpx(smoothed_points, 'out.gpx')


if __name__ == '__main__':
    main()

