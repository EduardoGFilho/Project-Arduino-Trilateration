

import numpy as np
import matplotlib.pyplot as plt

file_path = 'analyse_measurements\measurements\capture_us_function_of_distance.txt'  # Replace with your file path
data = np.loadtxt(file_path, dtype=np.uint64)

k = 340.29*1e-6*1e2*0.5
data_cm = data*k


means = []
vars = []

distances = np.arange(0,72.5,2.5)

for i in range(0,len(data) -5,5):
    means.append( np.mean(data_cm[i:i+5]))
    vars.append( np.var(data_cm[i:i+5]))


means = np.array(means)
vars = np.array(vars)

plt.figure()
plt.plot(distances,means,'k-o')
plt.plot(distances,distances,'b--')
plt.title("Measured Distance x Real distance")

plt.xlabel("Distance to sensor (cm)")
plt.legend(["Average measured distance (cm)","Real distance (cm)"])
plt.savefig("mean_wrt_distance")

plt.figure()
plt.title("Measurement Variance x Real distance")
plt.plot(distances,vars,'b-s')
plt.xlabel("Distance to sensor (cm)")
plt.legend(["Variance of measurements (cm$^2$)"])
plt.savefig("var_wrt_distance")
plt.show()



