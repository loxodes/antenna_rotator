# script to plot radiation pattern from anecohic chamber measurements 
from data_processing import *
import array_plot
import matplotlib.cm as cm
import pdb

TESTFILE = 'data/efgh_anecohic.hdf5'
TESTELEMENT = 'e' + GROUP_RADPAT
TESTFREQ = 2.49 * F_SCALE
TESTROT = 0 

if __name__ == "__main__":
    rots = range(-180,181,45)
    colors = iter(cm.rainbow(np.linspace(0,1,len(rots))))
    h5f = h5py.File(TESTFILE, 'r')

    pattern = get_radpattern(h5f, TESTELEMENT, TESTFREQ, 0)
    
    # get max gain, 
#pans = range(-90,91,10)
#   axial_ratio = []
#   for p in pans:
#       axial_ratio = axial_ratio + [get_axialratio(h5f, TESTELEMENT, TESTFREQ, p,0)] 
#   
#   scatter(pans, axial_ratio)
#   xlabel('antenna pan (degrees)')
#   ylabel('axial ratio (dB)')
#   title('measured axial ratio of WLP.2450.25.4.A.02 at ' + str(TESTFREQ/1e18) + 'GHz')
#   figure()   
    #subplot(3,1,3)
#   freqs = get_freqs(h5f)
#   axial_ratio = []
    #pdb.set_trace()
#   for f in freqs:
#       axial_ratio = axial_ratio + [get_axialratio(h5f, TESTELEMENT, f, 0,0)]
 
#   scatter([f / F_SCALE for f in freqs], axial_ratio)
#   xlabel('frequency (GHz)')
#   ylabel('axial ratio (dB)')
#   title('measured axial ratio of WLP.2450.25.4.A.02 at boresight')

    ax = array_plot.plot_sphere(pattern['gain'], pattern['phi'], pattern['theta'])

    ax.set_xlabel('antenna azimuth (degrees from boresight)')
    ax.set_ylabel('antenna eleveation (degrees from boresight)')
    ax.set_zlabel('anecohic chamber path loss (dB)')
    show()
