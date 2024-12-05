import numpy as np
import csv

def load_simu_data(path):

    arr = []
    with open(path, newline='') as csvfile:

        spamreader = csv.reader(csvfile, delimiter=',')

        for row in spamreader:
            arr.append(np.fromiter(row,dtype = float))

    a = np.array(arr)
    R0,R1,R2,X,Y = np.transpose(a)
    
    return R0,R1,R2,X,Y

# Use the equations for trilateration
def get_xy_trilateration(r0,r1,r2,x0,x1,x2,y0,y1,y2):
    A = -2*x0 + 2*x1
    B = -2*y0 + 2*y1 
    C = r0**2 - r1**2 -x0**2 + x1**2 - y0**2 +y1**2
    D = -2*x1 + 2*x2
    E = -2*y1 + 2*y2
    F = r1**2 - r2**2 -x1**2 + x2**2 - y1**2 +y2**2

    x_hat = (C*E - F*B) / (E*A - B*D)
    y_hat = (C*D - A*F) / (B*D - A*E)

    return x_hat,y_hat

# Note: we assume the dr is the same error for every measured distance,
# the estimation will still upper-bound the error if we chose the maximum
# dr possible.

def get_dxdy_model(dr,r0,r1,r2,x0,x1,x2,y0,y1,y2):
    A = -2*x0 + 2*x1
    B = -2*y0 + 2*y1 
    #C = r0**2 - r1**2 -x0**2 + x1**2 - y0**2 +y1**2
    D = -2*x1 + 2*x2
    E = -2*y1 + 2*y2
    #F = r1**2 - r2**2 -x1**2 + x2**2 - y1**2 +y2**2

    dC = 2*dr*r0 + 2*dr*r1
    dF = 2*dr*r1 - 2*dr*r2

    dx = (dC*np.abs(E) + dF*np.abs(B))/np.abs(E*A - B*D)
    dy = (dC*np.abs(D) + dF*np.abs(A))/np.abs(E*A - B*D)

    return dx, dy