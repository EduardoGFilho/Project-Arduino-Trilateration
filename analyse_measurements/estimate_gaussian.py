"""
This script takes in some measurements obtained with the HC-SR04 ultrassonic sensor
and uses them to estimate the mean and variance of the data
"""

import numpy as np
import matplotlib.pyplot as plt

def gaussian(sigma2,mu,x):
    g = (1/np.sqrt(sigma2*2*np.pi))*np.exp(-0.5*((x-mu)**2)/sigma2)
    return g

# Load the text file into a NumPy array, specifying unsigned long (np.uint64)
file_path = 'analyse_measurements\measurements\long_capture.txt'  # Replace with your file path
data = np.loadtxt(file_path, dtype=np.uint64)

k = 340.29*1e-6*1e2/2
data_cm = data*k

mean = np.mean(data_cm)
var = np.var(data_cm)

print(f"var = {var}, mean = {mean}")


num_bins = 10
num_samples = len(data)
bin_len = (np.max(data_cm) - np.min(data_cm))/num_bins
x = np.linspace(np.min(data_cm), np.max(data_cm), 100)
pdf = gaussian(var,mean,x)

counts, bins,_ = plt.hist(data_cm, num_bins)
plt.plot(x,pdf*num_samples*bin_len)
plt.title("Histogram and Scaled Gaussian PDF")
plt.legend(["Scaled PDF", "Histogram"])
plt.savefig("hist_and_gaussian")
plt.show()


