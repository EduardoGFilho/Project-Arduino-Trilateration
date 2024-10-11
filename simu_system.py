# This script is supposed to model, to the best degree we manage,

# Input is probably time instant, percourse, velocity, beacon positions, etc...

# Output has gotta be angle and distance to beacons

t = 0 # Time
n = 0 # Discrete time
# We could perhaps use a servo, then this parameter vanishes
w = 0 # Angular speed of motor
beamwidth = 120
beacon_thickness = 4 # 4cm of  diameter

# given time t,
phi = phi0 + t*w
# Check if there's a beacon within the beamwidth

# If so, get distance measurements and angle

# If there's nothing, just report null, 0, inf, or whatever error value

def look_at_beacon(phi0,t,w, beamwidth, beacon_position, beacon_thickness, my_position):
    phi = phi0 + t*w # Direction where sensor is pointed

    alpha_beacon = np.angle(beacon_position - my_position)
    distance_beacon = np.abs(beacon_position - my_position)

    #angle_interval= np.atan(beacon_thickness/(distance_beacon*2))

    if alpha_beacon - beamwidth/2 < phi < alpha_beacon - beamwidth/2:
        # commence measuring the distance

    # Use some magic to know if we'll get the echo or not

    # if measurement sucessfull, return measurement



