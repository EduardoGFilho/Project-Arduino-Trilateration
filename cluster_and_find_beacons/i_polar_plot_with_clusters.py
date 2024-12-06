import matplotlib.pyplot as plt
import numpy as np
from utils_clustering import load_measured_data
from cluster_samples import serial_cluster_samples

plt.ion()  # Turning interactive mode on

path_to_data = "cluster_and_find_beacons\capture_tri9.txt"
angles, distances = load_measured_data(path_to_data)
angles = angles *np.pi/180

# Plotting the first frame
fig = plt.figure()
ax = fig.add_subplot(projection='polar')
graph = ax.scatter(angles[0],distances[0])

i = 0
a = []
d = []

# Not really the first angle available, but the first one for which
# we start clustering
first_angle = angles[2]

dl2 = 0 # Last-by-2-distance
dl1 = 0 # Last-by-1-distance
dcurrent = 0

al = 0
acurrent = 0

color_counter = 0

current_cluster_a = []

current_cluster_d = []

last_cluster_mean_a = 0
last_cluster_mean_d = 0

# The update loop
while(True):

    # Reassign cyclic buffer
    dl2 = dl1
    dl1 = dcurrent
    dcurrent = distances[i]
    al = acurrent
    acurrent = angles[i]
    code  = serial_cluster_samples(dcurrent, dl1,dl2, alpha = 5)

    if i > 2: # Wait for enough valid data

        # The "current" sample is in fact the previous by one angle and distance,
        # "al" and "dl1"
        
        if code == 0: # Sample is trash
            graph = ax.scatter(al, dl1,marker = 'd', color = 'r', alpha = 0.8)

        elif code == 1: # Sample belongs to the current cluster
            graph = ax.scatter(al, dl1, color = plt.cm.tab10(color_counter), alpha = 0.8)
            current_cluster_a.append(al)
            current_cluster_d.append(dl1)
        elif code == 2: # Next sample belongs to next cluster
            # Plot the current sample
            graph = ax.scatter(al, dl1, color = plt.cm.tab10(color_counter), alpha = 0.8)
            current_cluster_a.append(al)
            current_cluster_d.append(dl1)
            
            # Calculate parameters of the current cluster
            if len(current_cluster_d)> 10:
                last_cluster_mean_a = np.angle(np.sum(np.exp(1j*np.array(current_cluster_a))))
                last_cluster_mean_d = np.mean(current_cluster_d)
                graph = ax.scatter(last_cluster_mean_a, last_cluster_mean_d, color = 'k', 
                                marker = 'x', s = 100, linewidths = 3)
                

            # Reset cluster
            color_counter += 1
            current_cluster_d = []
            current_cluster_a = []

    plt.ylim([0,130])
    # Calling pause function for 0.25 seconds
    plt.pause(0.25)

    # Uncomment this line to save evolution over time of the sensor
    #plt.savefig(f"cluster_and_find_beacons\clustering_frames\clustering{i}.png")

    if (first_angle == acurrent) and i > 2:
        graph = ax.scatter(angles[0],distances[0])
        plt.cla()
        color_counter = 0
        i = 0
        a = []
        d = []
        current_cluster_d = []
        current_cluster_a = []

    i+=1
