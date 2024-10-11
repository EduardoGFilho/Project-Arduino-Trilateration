import numpy as np


# Inputs are complex numbers, beamwidth and phi are in radians
def get_delay(my_position, beacon_positions, beamwidth, phi):
    distances = beacon_positions - my_position
    angles = np.angle(distances)
    d = np.abs(distances)

    # Check if any beacons are in sight

    visible = np.abs(angles - phi) < beamwidth/2

    # If we see nothing
    if not np.any(visible):
        return 0,0

    # Find the visible beacon

    visible_d = d[visible]
    visible_a = angles[visible]

    # speed of sound == 340.29 m / s
    SPEED_OF_SOUND = 34029 # speed of sound in cm/s
    delay = 2*visible_d*SPEED_OF_SOUND

    return delay, visible_a


if __name__ == "__main__":

    # Beacon positions
    k = 20 # Distance between beacons

    x0, y0 = k*np.array([0,0])
    x1, y1 = k*np.array([1,0])
    x2, y2 = k*np.array([0,1])
    x3, y3 = k*np.array([1,1])

    b1 = x1 + 1j*y1
    b2 = x2 + 1j*y2
    b3 = x3 + 1j*y3

    beacons = np.array([b1,b2,b3])

    # Path is a simple line from (10,0) to (10,20)

    Ts = 60 # Sampling period, set to wharever value for now
    speed = 20/30 # 20 cm/ 30 s

    N = int(np.ceil((20/speed) * Ts))
    n = np.arange(0,N+1)
    t = Ts*n

    # Position in terms of time
    y = t*speed

    pos = 10 + 1j*y

    # Establish how phi evolves in time
    num_angle_samples = 10

    # At first we assume the robot only takes a step after every measurement, which is stupid
    # TODO: the robot moves AS the sensor spins. also: The evolution of phi is more important
    # than the evolution of the position

    #phis = np.pi*2/num_angle_samples
    phis = np.arange(num_angle_samples)*np.pi*2/num_angle_samples

    delays = np.zeros((N,num_angle_samples))
    alphas = np.zeros((N,num_angle_samples))
    for i in range(N):
        for j in range(len(phis)):
            # TODO: implement "something" for when we get two echoes, because in real life
            # we won't be able to tell which's which
            delay, a = get_delay(pos[i],beacons,beamwidth= 70*np.pi/180, phi = phis[j])

            delays[i,j] = delay
            alphas[i,j] = a

    print(delays[0,:])
    print(alphas[0,:])

    


    


