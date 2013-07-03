# functions to plot data from array measurements

from pylab import *
from enthought.mayavi import mlab

# 3d plot of antenna pattern given gain, pan, and tilt
# see http://matplotlib.org/examples/mplot3d/trisurf3d_demo.html
def plot_sphere(r, phi, theta):
    x = r*sin(phi)*cos(theta)
    y = r*cos(phi)
    z = r*sin(phi)*sin(theta)
   
    fig = figure()

    ax = fig.gca(projection='3d')
    ax.plot_trisurf(x, y, z, cmap=cm.jet, linewidth=0.2)

    show()

# to plot...
# maximum gain at each pan and tilt, z axis gain, color is axial ratio
