"""
This script generates some data meant to represent what the distance sensor
captures, assuming the beacons are classified flawlessly
"""


import numpy as np
from numpy.random import randn, rand
import csv

# Calculate distance between two points and add noise
def get_radius(x,y,x0,y0,noise_var = 0):
    r = np.sqrt((x-x0)**2 + (y-y0)**2)
    r = r + np.sqrt(noise_var)*randn()
    return r

if __name__ == "__main__":

    n = 0.01 # Noise power
    n_rows = 10 # Number of rows

    # Beacon positions
    k = 50 # Distance between beacons

    x0, y0 = k*np.array([0,0])
    x1, y1 = k*np.array([1,0])
    x2, y2 = k*np.array([0,1])
    x3, y3 = k*np.array([1,1])

    with open(f'./synthetic_data_n={n}.csv', 'w', newline='') as csvfile:

        writer = csv.writer(csvfile, delimiter=',')
        
        for i in range(n_rows):
            # Unit is cm, so 50 cm of range
            x, y = 50*rand(2)
            #position_noisy = position + np.sqrt(n)*randn(2)
            r0 = get_radius(x,y,x0,y0,n)
            r1 = get_radius(x,y,x1,y1,n)
            r2 = get_radius(x,y,x2,y2,n)
            r3 = get_radius(x,y,x3,y3,n)
            
            # Note: we don't save the r3
            writer.writerow([r0,r1,r2,x,y])