# Code from chatGPT

import matplotlib.pyplot as plt
import numpy as np

# Function to calculate the distance between two points
def distance(point1, point2):
    return np.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)

# Define two points
point1 = (1, 1)
point2 = (4, 3)

# Calculate the distance between the two points (this will be the radius of the circle)
radius = distance(point1, point2)

# Create a figure and axis
fig, ax = plt.subplots()

# Plot the first point
ax.plot(point1[0], point1[1], 'bo', label='Point 1 (Center)')

# Plot the second point
ax.plot(point2[0], point2[1], 'ro', label='Point 2 (Perimeter)')

# Create the circle with center at point1 and radius equal to the distance between point1 and point2
circle = plt.Circle(point1, radius, color='g', fill=False, linestyle='--')

# Add the circle to the plot
ax.add_artist(circle)

# Set the aspect ratio of the plot to be equal, so the circle isn't distorted
ax.set_aspect('equal', 'box')

# Add grid, labels, and title
plt.grid(True)
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Two Points and a Circle')

# Add a legend
plt.legend()

# Set limits for the plot to ensure the entire circle and points are visible
ax.set_xlim(min(point1[0], point2[0]) - radius, max(point1[0], point2[0]) + radius)
ax.set_ylim(min(point1[1], point2[1]) - radius, max(point1[1], point2[1]) + radius)

# Show the plot
plt.show()
