import numpy as np
from numpy.linalg import norm, inv
from numpy.random import randn
import csv


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

    data = load_data("synthetic_data_n=4.csv")
    # position of beacons

    p0 = np.array((10,10))
    p1 = np.array((0,0))
    p2 = np.array((0,10))
    p3 = np.array((10,0))

    # position of "agent"

    n = 1

    p = np.array((28.4567,20.456789)) #+ np.sqrt(n)*randn(2)

    # For now, just calculate the distance, later make a different script which can
    # add noise and other stuff

    r0 = norm(p - p0) + np.sqrt(n)*randn()
    r1 = norm(p - p1) + np.sqrt(n)*randn()
    r2 = norm(p - p2) + np.sqrt(n)*randn()
    r3 = norm(p - p3) + np.sqrt(n)*randn()

    x0, y0 = p0
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3

    #https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5461075/

    A = 2*np.array( [[x0 - x3, y0 - y3],
                    [x1 - x3, y1 - y3],
                    [x2 - x3, y2 - y3]])

    b = np.array([[ x0**2 - x3**2 + y0**2 - y3**2 + r3**2 - r0**2],
                    [x1**2 - x3**2 + y1**2 - y3**2 + r2**2 - r0**2],
                    [x2**2 - x3**2 + y2**2 - y3**2 + r1**2 - r0**2]])


    A = np.matrix(A)
    b = np.matrix(b)

    x = inv(A.T * A)* (A.T * b)

    x[0] = 10 -x[0]
    print(x)