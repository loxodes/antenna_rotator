from pylab import *
from hdf5_tools import *
import h5py
from skrf import complex_2_degree
from analyze_phaseatt import *

FILENAME = 'efgh_insitu_postcal'
TESTELEMENTS = ['e', 'f','g', 'h']#'h', 'e', 'f']
ELEMENTCOLORS = ['red', 'blue', 'yellow', 'brown', 'pink']
TESTFREQ = 2.485e18 # mHz
FSWEEPLOC = 'vna_frequencysweep'
ATT_REF = 14.8

if __name__ == "__main__":

    hd5file = h5py.File(FILEPREFIX + FILENAME + '.hdf5', 'r')
    for (i, e) in enumerate(TESTELEMENTS):
        print e
        phase = get_phase(hd5file, e[0], TESTFREQ)#, group = GROUP_RAWPHASE)
        att = get_att(hd5file, e[0], TESTFREQ)#, group = GROUP_RAWATT)
        
        
        subplot(2,1,1)
#/title('measured phase and attenuation of revision 3 t/r modules before and after matching network tuning')
#scatter(phase['phase_target'], [(phase['phase_measured'][j] - phase['phase_target'][j]) % 360 for j in range(len(phase['phase_target']))], color=ELEMENTCOLORS[i])
        phase_errors =  (np.array(phase['phase_measured']) - np.array(phase['phase_target'])) % 360
        phase_errors = np.array([p - 360 * (p > 180) for p in phase_errors])
        att_errors = np.array(phase['att_measured'] - ATT_REF)
        print 'rms phase error: ' + str(sqrt(mean(phase_errors**2)))
        print 'rms amplitude error: ' + str(sqrt(mean(att_errors**2)))
        scatter(phase['phase_target'], phase_errors, color=ELEMENTCOLORS[i])#[(phase['phase_measured'][j] - phase['phase_target'][j] * -5.6) % 360 for j in range(len(phase['phase_target']))], color=ELEMENTCOLORS[i])
        xlabel('target phase shift (degrees)')
        ylabel('phase error (degrees)')
        title('Measured phase error through phased array modules with target phase shift after calibration.')
        ylim([-12,12])
        xlim([0,360])
        
        legend(TESTELEMENTS)
        subplot(2,1,2)
        scatter(phase['phase_target'], att_errors, color=ELEMENTCOLORS[i])
        xlabel('target phase shift (degrees)')
        ylabel('measured gain error (dB)')
        title('Measured gain error through phased array modules with target phase shift after calibration.')
        ylim([-1,1])
        xlim([0,360])
        
        legend(TESTELEMENTS)

        
    hd5file.close()
    show()
