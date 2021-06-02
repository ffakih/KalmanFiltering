#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 27 16:25:03 2021

@author: firasfakih
"""
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pykalman import KalmanFilter
from statsmodels.nonparametric.smoothers_lowess import lowess

pd.plotting.register_matplotlib_converters()

arg1 = sys.argv[1]
cpu_data = pd.read_csv(arg1,parse_dates = ['timestamp'])

# loess smoothing, frac 0.02 to account for the expected high values
loess_smoothed = lowess(cpu_data['temperature'],cpu_data['timestamp'],frac = 0.015)


# kalman filtering
kalman_data = cpu_data[['temperature', 'cpu_percent', 'sys_load_1', 'fan_rpm']]
initial_state = kalman_data.iloc[0]
observation_covariance = np.diag([3, 3, 3, 3]) ** 2
transition_covariance = np.diag([.4, .4, .4, .4]) ** 2 
transition = [[0.97,0.5,0.2,-0.001], [0.1,0.4,2.2,0], [0,0,0.95,0], [0,0,0,1]] 

kf = KalmanFilter(initial_state_mean=initial_state,
    initial_state_covariance=observation_covariance,
    observation_covariance=observation_covariance,
    transition_covariance=transition_covariance,
    transition_matrices=transition
)
kalman_smoothed, _ = kf.smooth(kalman_data)


plt.figure(figsize=(12, 4))
plt.plot(cpu_data['timestamp'], cpu_data['temperature'], 'b.', alpha=0.5)
plt.plot(cpu_data['timestamp'], kalman_smoothed[:, 0], 'g-', label="Kalman Smoothing")
plt.plot(cpu_data['timestamp'], loess_smoothed[:, 1], 'r-', label="LOESS Smoothing")
plt.legend()
plt.savefig('cpu.svg') # for final submission


