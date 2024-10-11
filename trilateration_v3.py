import numpy as np
import matplotlib.pyplot as plt
import csv
from random_data import get_radius



def load_data(path):

    arr = []
    with open(path, newline='') as csvfile:

        spamreader = csv.reader(csvfile, delimiter=',')

        for row in spamreader:
            arr.append(np.fromiter(row,dtype = float))

    a = np.array(arr)
    R0,R1,R2,R3,X,Y = np.transpose(a)
    
    return R0,R1,R2,R3,X,Y

if __name__ == "__main__":

    R0,R1,R2,R3,X,Y = load_data("synthetic_data_n=0.5.csv")

    R0,R1,R2,R3,X,Y = np.array([R0,R1,R2,R3,X,Y])[:,40:60]


    # Beacon positions
    k = 10 # Distance between beacons

    x0, y0 = k*np.array([0,0])
    x1, y1 = k*np.array([1,0])
    x2, y2 = k*np.array([0,1])
    x3, y3 = k*np.array([1,1])


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

    # TODO: Search if it's worth it to find the pdf of error when assuming
    # sensor measurements are contaminated by white noise

    E_y = np.abs(Y_hat - Y)
    E_x = np.abs(X_hat - X)

    E = np.sqrt(E_y**2 + E_x**2)

    #print(Y[0],Y_hat[0],X[0], X_hat[0])
    print(E[:10])

    # Below is code from chatGPT

    # Create a figure and axis
    fig, ax = plt.subplots()

    # Plot the first point
    ax.plot(X, Y, 'bo', label='Actual position')

    # Plot the second point
    ax.plot(X_hat, Y_hat, 'ko', label='Estimated position')

    R = get_radius(X,Y,X_hat,Y_hat)

    for i in range(len(X)):
        # Create the circle with center at point1, radius, filled, and with transparency
        circle = plt.Circle((X[i],Y[i]), R[i], color='r', alpha=0.3, fill=True)

        # Add the circle to the plot
        ax.add_artist(circle)

    # Set the aspect ratio of the plot to be equal, so the circle isn't distorted
    ax.set_aspect('equal', 'box')

    # Add grid, labels, and title
    plt.grid(True)
    plt.xlabel('X-axis (cm)')
    plt.ylabel('Y-axis (cm)')
    plt.title('Trilateration Error Visualization, Synthetic Data N = 0.5')

    # Add a legend
    plt.legend()

    # Set limits for the plot to ensure the entire circle and points are visible
    ax.set_xlim(-10, 60)
    ax.set_ylim(-10,60)

    # Show the plot
    plt.show()
