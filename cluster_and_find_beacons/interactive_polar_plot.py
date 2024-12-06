import matplotlib.pyplot as plt
from utils_clustering import load_measured_data
import numpy as np

plt.ion()  # turning interactive mode on

path_to_data = "cluster_and_find_beacons\capture_tri9.txt"
angles, distances = load_measured_data(path_to_data)
angles = angles *np.pi/180

# plotting the first frame
fig = plt.figure()
ax = fig.add_subplot(projection='polar')
graph = ax.scatter(angles[0],distances[0])

i = 0
a = []
d = []

first_angle = angles[0]
cutting_distance = 130

# Update loop
while(True):
    # Update the data
    a.append(angles[i])
    d.append(distances[i])

    
    # Removing the older graph
    graph.remove()
    # Plotting newer graph
    graph = ax.scatter(a,d, color = plt.cm.tab10(0), alpha = 0.8)
    plt.ylim([0,cutting_distance])
    
    # Calling pause function for 0.25 seconds
    plt.pause(0.25)

    # Restart after a full revolution
    if (first_angle == a[-1]) and i > 0:
        i = 0
        a = []
        d = []

    i+=1