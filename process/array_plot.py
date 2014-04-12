# functions to plot data from array measurements

from pylab import *
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.cm as cm
from mayavi import mlab
from data_processing import *
import pdb

COLORS = ['red', 'blue', 'purple', 'brown']

def plot_radarraysurf(pattern):
    fig = figure()
    ax = Axes3D(fig) 
    thetas = pattern['thetas']
    phis = pattern['phis']
    pattern_maxgain = np.zeros([len(thetas), len(phis)])
    pattern_axialratio = np.zeros([len(thetas), len(phis)])

    for i in range(len(thetas)):
        for j in range(len(phis)):
            pattern_maxgain[i,j] = max(pattern['radarray_gain'][i,j,:])
    
    theta_mat, phi_mat = meshgrid(thetas,phis)

    r = pattern_maxgain.transpose()
    phi = deg2rad(phi_mat)
    theta = deg2rad(theta_mat)

    surf = ax.plot_surface(theta_mat, phi_mat, (pattern_maxgain).transpose(), rstride=1, cstride=1, cmap=cm.coolwarm)
    
    ax.set_xlabel('antenna azimuth (degrees from boresight)')
    ax.set_ylabel('antenna eleveation (degrees from boresight)')
    ax.set_zlabel('anecohic chamber path gain (dB)')
    cb = fig.colorbar(surf, shrink=0.5, aspect=5)
    cb.set_label('anecohic chamber path gain (dB)')

    show()
    return ax

def plot_arrayslices(pattern, offset = 0, dash = '-', elsteers = [0,3,6]):
    thetas = pattern['thetas']
    phis = pattern['phis']
    pattern_maxgain = np.zeros([len(thetas), len(phis)])
    pattern_axialratio = np.zeros([len(thetas), len(phis)])

    
    for i in range(len(thetas)):
        for j in range(len(phis)):
#            if sum(pattern['radarray_gain'][i,j,:]) != 0:
            pattern_maxgain[i,j] = get_axialratio(pattern['rots'],pattern['radarray_mag'][i,j,:])['directivity'] + offset
     
    radpat = pattern_maxgain.transpose()
    for (i,el) in enumerate(elsteers):
        plot(thetas, radpat[el,:], dash, linewidth=3, color=COLORS[i])

#    legend(elsteers, title='Elevation Angle\nOrientation (degrees)',fancybox=True)


def plot_radarray_polar(pattern):
    # attempt to use mayavi to generate polar plot of radiation pattern slice
    fig = figure()
    
    thetas = pattern['thetas']
    phis = pattern['phis']
    pattern_maxgain = np.zeros([len(thetas), len(phis)])
    pattern_axialratio = np.zeros([len(thetas), len(phis)])

    for i in range(len(thetas)):
        for j in range(len(phis)):
            pattern_maxgain[i,j] = max(pattern['radarray_gain'][i,j,:])
    
    theta_mat, phi_mat = meshgrid(thetas,phis)

    r = pattern_maxgain.transpose()
    phi = deg2rad(phi_mat)
    theta = deg2rad(theta_mat)


    x = r*sin(phi)*cos(theta)
    y = r*cos(phi)
    z = r*sin(phi)*sin(theta)

    s = mlab.mesh(x, y, z)
   
    show()
    return ax


