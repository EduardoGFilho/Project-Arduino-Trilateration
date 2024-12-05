"""
This script runs the trilateration algorithm over some data and then illustrates in a plot
the caculated error
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import collections
from generate_random_data import get_radius
from utils import load_simu_data, get_dxdy_model

if __name__ == "__main__":

    R1,R2,R3,X,Y = load_simu_data("synthetic_data_n=0.5.csv")

    # Beacon positions
    k = 50 # Distance between beacons

    x1, y1 = k*np.array([0,0])
    x2, y2 = k*np.array([1,0])
    x3, y3 = k*np.array([0,1])
    #x3, y3 = k*np.array([1,1])


    # https://math.stackexchange.com/questions/884807/find-x-location-using-3-known-x-y-location-using-trilateration#884851

    X1 = x1*np.ones_like(R1)
    X2 = x2*np.ones_like(R1)
    X3 = x3*np.ones_like(R1)

    Y1 = y1*np.ones_like(R1)
    Y2 = y2*np.ones_like(R1)
    Y3 = y3*np.ones_like(R1)

    A = -2*X1 + 2*X2
    B = -2*Y1 + 2*Y2 
    C = R1**2 - R2**2 -X1**2 + X2**2 - Y1**2 +Y2**2
    D = -2*X2 + 2*X3
    E = -2*Y2 + 2*Y3
    F = R2**2 - R3**2 -X2**2 + X3**2 - Y2**2 +Y3**2

    X_hat = (C*E - F*B) / (E*A - B*D)
    Y_hat = (C*D - A*F) / (B*D - A*E)

    E_y = np.abs(Y_hat - Y)
    E_x = np.abs(X_hat - X)

    E = np.sqrt(E_y**2 + E_x**2)

    print(E[:10])

    # Below is code from chatGPT, to plot the data

    # Create a figure and axis
    fig, ax = plt.subplots()

    ax.plot([x1, x2, x3],[y1, y2, y3],"s",color = "gray",markersize = 10, label = "Beacons")

    # Plot the first points
    ax.plot(X, Y, 'bo', label='Actual position')

    # Plot the estimated points
    ax.plot(X_hat, Y_hat, 'ko', label='Estimated position')

    R = get_radius(X,Y,X_hat,Y_hat)

    dx = np.abs(X - X_hat)
    dy = np.abs(Y - Y_hat)

    # 3*std_dev == 99% accuracy
    dx2,dy2 = get_dxdy_model(3*np.sqrt(0.5),R1,R2,R3,X1,X2,X3,Y1,Y2,Y3)

    coll = collections.EllipseCollection(dx, dy,np.zeros_like(R), offsets=np.transpose([X,Y]),
                                        units='x', color = "red", alpha = 0.4, offset_transform=ax.transData,
                                        label = "Error Radius Calculated")
    ax.add_collection(coll)

    coll = collections.EllipseCollection(dx2, dy2,np.zeros_like(R), offsets=np.transpose([X,Y]),
                                        units='x', color = "green", alpha = 0.4, offset_transform=ax.transData,
                                        label = "Error Radius Model")
    ax.add_collection(coll)

    # Add a legend
    ax.legend()

    # Set the aspect ratio of the plot to be equal, so the circle isn't distorted
    ax.set_aspect('equal', 'box')

    # Add grid, labels, and title
    plt.grid(True)
    plt.xlabel('X-axis (cm)')
    plt.ylabel('Y-axis (cm)')
    plt.title('Trilateration Error Visualization, Synthetic Data N = 0.5')

    # Set limits for the plot to ensure the entire circle and points are visible
    ax.set_xlim(-10, 60)
    ax.set_ylim(-10,60)

    # Show the plot
    plt.show()
