import numpy as np
from numpy.random import rand
import csv

# This function returns completely inadequate data, only for the purpose
# of checking code execution and such
def load_data_fake(n):
    return rand(n), rand(n)

def load_measured_data(path):

    arr = []
    with open(path, newline='') as csvfile:

        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            arr.append(np.fromiter(row,dtype = float))

    a = np.array(arr)
    angle, distance = np.transpose(a)
    
    return angle, distance