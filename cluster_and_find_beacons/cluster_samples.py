# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 12:04:23 2024

@author: Eduardo
"""

import numpy as np
from utils_clustering import load_measured_data

# Input should have angles as strictly increasing function
# (because of trig, 360 to 1 is considered increasing)

def cluster_samples(angles, distances, alpha):

    trash = []
    clusters = []

    current_cluster = []

    # First case, exceptional
    close_to_nxt = abs(distances[0] - distances[1]) < alpha
    close_to_last = False

    if(close_to_nxt):
        current_cluster.append([angles[0], distances[0]])
    else:
        trash.append([angles[0], distances[0]])

    for i in range(1, len(angles) - 1):
        close_to_last = abs(distances[i] - distances[i-1]) < alpha
        close_to_nxt = abs(distances[i] - distances[i+1]) < alpha

        ctl = close_to_last
        ctn = close_to_nxt

        if(not ctl and not ctn):
            trash.append([angles[i], distances[i]])

        elif(not ctl and ctn):
            current_cluster = np.array(current_cluster)
            clusters.append(current_cluster)
            current_cluster = []
            current_cluster.append([angles[i], distances[i]])

        else:
            current_cluster.append([angles[i], distances[i]])

    # Last case, exceptional
    close_to_nxt = False
    close_to_last = abs(distances[-1] - distances[-2]) < alpha

    if(close_to_last):
        current_cluster.append([angles[-1], distances[-1]])
    else:
        trash.append([angles[-1], distances[-1]])

    current_cluster = np.array(current_cluster)
    clusters.append(current_cluster)

    # Casting
    trash = np.array(trash)

    return trash, clusters


# code == 0: l1 sample is trash
# code == 1: l1 sample belongs to current cluster 
# code == 2: l1 sample belongs to next cluster

def serial_cluster_samples(d_current, d_l1, d_l2, alpha):

        ctl = abs(d_l1 - d_current) < alpha
        ctn = abs(d_l1 - d_l2) < alpha

        if(not ctl and not ctn):
            return 0
        
        elif(not ctl and ctn):
            return 2
        
        else:
            return 1
        
def next_idx(current_idx, max_idx):
    next_idx = current_idx + 1

    if next_idx < max_idx:
        return next_idx
    else:
        return 0

def last_idx(current_idx, max_idx):

    if current_idx == 0:
        return max_idx - 1
    else:
        return current_idx - 1

if __name__ == "__main__":
    import matplotlib.pyplot as plt

    path_to_data = "cluster_and_find_beacons/capture_tri9.txt"
    angles, distances = load_measured_data(path_to_data)
    angles = angles *np.pi/180

    alpha = 4

    trash, clusters = cluster_samples(angles, distances, alpha)

    fig = plt.figure()
    ax = fig.add_subplot(projection='polar')
    #c = ax.scatter(np.pi - angles, distances)

    if len(trash) != 0:
        ax.scatter(trash[:, 0], trash[:, 1], marker='d', c='r')

    for cluster in clusters:
        a = np.array(cluster[:, 0])
        d = np.array(cluster[:, 1])
        ax.scatter(a, d)

    #ax.set_thetamin(0)
    #ax.set_thetamax(180)
    plt.title("Measured Positions")
    plt.show()
