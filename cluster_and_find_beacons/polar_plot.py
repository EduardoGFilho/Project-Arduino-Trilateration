import numpy as np
import matplotlib.pyplot as plt
from utils_clustering import load_data_fake, load_measured_data


if __name__ == "__main__":
    path_to_data = "cluster_and_find_beacons\capture_tri9.txt"
    angles, distances = load_measured_data(path_to_data)
    angles = angles *np.pi/180

    cutting_distance = 130

    # Discard measurings that are too far away
    angles = angles[distances<cutting_distance]
    distances = distances[distances<cutting_distance]

    # Polar plot of measurements:
    fig = plt.figure()
    ax = fig.add_subplot(projection='polar')
    #c = ax.scatter(angles, distances)
    c = ax.scatter(np.pi - angles, distances)
    ax.set_thetamin(0)
    ax.set_thetamax(180)
    plt.title("Measured Positions")

    plt.show()
