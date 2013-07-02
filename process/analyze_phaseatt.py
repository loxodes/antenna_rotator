from pylab import *
from hdf5_tools import *
import h5py
from skrf import complex_2_degree

FILEPREFIX = 'data/' 
FILENAME = 'efgh_preant'
TESTELEMENTS = ['e', 'f','g', 'h']#'h', 'e', 'f']
ELEMENTCOLORS = ['red', 'blue', 'yellow', 'brown', 'pink']

TESTFREQ = 2.485e18 # mHz
FSWEEPLOC = 'vna_frequencysweep'

def get_phase(hd5file, element, freq, group = GROUP_PHASE):
    fidx = get_fidx(hd5file, freq, FSWEEPLOC)
    
    phase_target = []
    phase_measured = []
    att_measured = []

    for phase in hd5file[element + group].keys():
        dset = element + group + '/' + phase 
        phase_measured = phase_measured + [complex_2_degree(hd5file[dset][fidx])]
        phase_target = phase_target + [int(hd5file[dset].attrs['phase'])]
        att_measured = att_measured + [20*log10(abs(hd5file[dset][fidx]))]
 
    att_measured = sort_by_array(phase_target, att_measured)
    phase_measured = sort_by_array(phase_target, phase_measured)
    phase_target = sort(phase_target)

    return {'phase_measured':phase_measured, 'phase_target':phase_target, 'att_measured':att_measured} 

def get_att(hd5file, element, freq, group = GROUP_ATT):
    fidx = get_fidx(hd5file, freq, FSWEEPLOC) 
    
    att_target = []
    att_measured = []
    phase_measured = []

    for att in hd5file[element + group].keys():
        dset = element + group + '/' + att 
        att_measured = att_measured + [20*log10(abs(hd5file[dset][fidx]))]
        att_target = att_target + [int(hd5file[dset].attrs['att'])]
        phase_measured = phase_measured + [complex_2_degree(hd5file[dset][fidx]) % 360]
        
    att_measured = sort_by_array(att_target, att_measured)
    phase_measured = sort_by_array(att_target, phase_measured)
    att_target = sort(att_target)
    return {'att_measured':att_measured, 'att_target':att_target, 'phase_measured':phase_measured}

if __name__ == "__main__":

    hd5file = h5py.File(FILEPREFIX + FILENAME + '.hdf5', 'r')
    for (i, e) in enumerate(TESTELEMENTS):
        print e
        phase = get_phase(hd5file, e[0], TESTFREQ)#, group = GROUP_RAWPHASE)
        att = get_att(hd5file, e[0], TESTFREQ)#, group = GROUP_RAWATT)
        
        
        subplot(2,2,1)
#/title('measured phase and attenuation of revision 3 t/r modules before and after matching network tuning')
#scatter(phase['phase_target'], [(phase['phase_measured'][j] - phase['phase_target'][j]) % 360 for j in range(len(phase['phase_target']))], color=ELEMENTCOLORS[i])
        
        scatter(phase['phase_target'], (np.array(phase['phase_measured']) - np.array(phase['phase_target'])) % 360, color=ELEMENTCOLORS[i])#[(phase['phase_measured'][j] - phase['phase_target'][j] * -5.6) % 360 for j in range(len(phase['phase_target']))], color=ELEMENTCOLORS[i])
        xlabel('target phase (degrees)')
        ylabel('phase error (degrees)')

        subplot(2,2,2)
        scatter([at/4.0 for at in att['att_target']], att['att_measured'], color=ELEMENTCOLORS[i])
        xlabel('target attenuation (dB)')
        ylabel('measured attenuation')

        legend(TESTELEMENTS)
        subplot(2,2,3)
        scatter(att['att_target'], att['phase_measured'], color=ELEMENTCOLORS[i])
        xlabel('attenuation register value')
        ylabel('measured phase shift (degrees)')
        
        subplot(2,2,4)
        scatter(phase['phase_target'], phase['att_measured'], color=ELEMENTCOLORS[i])
        xlabel('phase shifter register value')
        ylabel('measured gain (dB)')
    

        
    hd5file.close()

    show()
