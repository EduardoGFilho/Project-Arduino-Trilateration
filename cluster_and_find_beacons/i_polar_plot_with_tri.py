import matplotlib.pyplot as plt
import numpy as np
from utils_clustering import load_measured_data
from cluster_samples import serial_cluster_samples
from utils import get_xy_trilateration, get_dxdy_model

# Beacon Positions:

x1, y1 = 75.3,42.2
x2, y2 = 42.6,69.5
x3, y3 = 2.8, 41.7

# x,y = 38.2, 10.2

min_n_samples = 10
max_distance = 85

# Approximate angular position of the beacons,
a1 = 30*np.pi/180 
a2 = 90*np.pi/180 
a3 = 130*np.pi/180 

plt.ion()  # Turning interactive mode on

path_to_data = "cluster_and_find_beacons\data(2).txt"
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

beacons_d = []
beacons_a = []


if __name__ == "__main__":

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
                
                ## Calculate parameters of the current cluster

                # Ignore too few data or range farther than we know the beacons are
                if len(current_cluster_d)> min_n_samples and current_cluster_d[0]< max_distance:
                    last_cluster_mean_a = np.angle(np.sum(np.exp(1j*np.array(current_cluster_a))))
                    last_cluster_mean_d = np.mean(current_cluster_d)
                    graph = ax.scatter(last_cluster_mean_a, last_cluster_mean_d, color = 'k', 
                                    marker = 'x', s = 100, linewidths = 3)
                    
                    beacons_d.append(last_cluster_mean_d)
                    beacons_a.append(last_cluster_mean_a)

                # Reset cluster
                color_counter += 1
                current_cluster_d = []
                current_cluster_a = []

        plt.ylim([0,max_distance])
        # Calling pause function for 0.25 seconds
        plt.pause(0.005)


        # Uncomment this line to save evolution over time of the sensor
        #plt.savefig(f"cluster_and_find_beacons\clustering_frames\clustering_full_sys{i}.png")

        if (first_angle == acurrent) and i > 2:
            break
        i+=1

    plt.savefig(f"cluster_and_find_beacons\clustering_full_sys.png")
        
    # We'll just assume everything worked out and we found the three beacons
    beacons_a = np.array(beacons_a)

    r1 = beacons_d[np.argmin(np.abs(a1 - beacons_a))]
    r2 = beacons_d[np.argmin(np.abs(a2 - beacons_a))]
    r3 = beacons_d[np.argmin(np.abs(a3 - beacons_a))]

    # We chose the uncertainty to be 3 times the std. deviation
    dr = 0.5 # Quantization error

    x,y = get_xy_trilateration(r1,r2,r3,x1,x2,x3,y1,y2,y3)
    dx,dy = get_dxdy_model(dr,r1,r2,r3,x1,x2,x3,y1,y2,y3)

    print(f"Beacon angles (rad):{beacons_a}")
    print(f"Beacon distances (cm):{beacons_d}")
    print(f"Estimated position (x,y) == ({x},{y})")
    print(f"Estimated positioning error (dx,dy) == ({dx},{dy})")
    plt.show()
