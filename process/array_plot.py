# functions to plot data from array measurements

from pylab import *
from enthought.mayavi import mlab

# 3d plot of antenna pattern given gain, pan, and tilt
def plot_sphere(gain, phi, theta):
    r = gain
    x = r*sin(phi)*cos(theta)
    y = r*cos(phi)
    z = r*sin(phi)*sin(theta)

    s = mlab.mesh(x, y, z)
    mlab.show()

