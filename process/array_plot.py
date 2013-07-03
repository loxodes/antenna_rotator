# functions to plot data from array measurements

from pylab import *
from mpl_toolkits.mplot3d import Axes3D

# 3d plot of antenna pattern given gain, pan, and tilt
# see http://matplotlib.org/examples/mplot3d/trisurf3d_demo.html
def plot_sphere(r, phi, theta):
    #x = r*sin(phi)*cos(theta)
    #y = r*cos(phi)
    #z = r*sin(phi)*sin(theta)
   
    fig = figure()

    ax = fig.gca(projection='3d')
    #x.scatter3D(x, y, z, cmap=cm.jet) # plot trisurf
    ax.plot_trisurf(phi, theta, r, cmap=cm.jet)
    ax.set_aspect('equal', 'datalim')
    return ax
# to plot...
# maximum gain at each pan and tilt, z axis gain, color is axial ratio
