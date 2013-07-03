# script to plot radiation pattern from anecohic chamber measurements 
from data_processing import *
import matplotlib.cm as cm
import pdb

TESTFILE = 'data/efgh_anecohic.hdf5'
TESTELEMENT = 'e' + GROUP_RADPAT
TESTFREQ = 2.49 * F_SCALE
TESTROT = 0 

if __name__ == "__main__":
    #rots = [150, -30, 60, -120]
    rots = range(-180,181,45)
    #subplot(4,2,1)
    #pattern = get_radpattern(TESTFILE, TESTELEMENT + GROUP_RADPAT, TESTFREQ, TESTROT)
    colors = iter(cm.rainbow(np.linspace(0,1,len(rots))))
    h5f = h5py.File(TESTFILE, 'r')

    for i in rots:
        pattern = get_radpattern(h5f, TESTELEMENT, TESTFREQ, i)
        scatter(pattern['theta'], pattern['gain'],color=next(colors))

    legend([str(r) for r in rots])
    xlabel('antenna pan (degrees)')
    ylabel('|S21| (dB)')
    title('measured |S21| of WLP.2450.25.4.A.02 at ' + str(TESTFREQ/1e18) + 'GHz with varying roll')
#    figure()
    #subplot(4,2,2)
    
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
    

    show()

    #array_plot.plot_sphere(pattern['gain'], pattern['phi'], pattern['theta'])
