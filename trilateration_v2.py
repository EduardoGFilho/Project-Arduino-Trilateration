"""
This script runs the trilateration algorithm over some data and then prints the calculated
"""

import numpy as np
from utils import load_simu_data

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
    