from analyze_phaseatt import *
from analyze_trmodule import *
import pdb


FILEPREFIX = 'data/'
TESTELEMENTS = ['e_cal', 'f_cal', 'g_cal', 'h_cal']
ELEMENTCOLORS = ['red', 'blue', 'yellow', 'brown', 'pink']


if __name__ == "__main__":
    frequency = 2.485e9

    for (i, fname) in enumerate(TESTELEMENTS):
        h5f = h5py.File(FILEPREFIX + fname + '.hdf5', 'r') 
        subplot(3,1,1)
        pins = get_pins(h5f, 'txpath')
        pae = get_pae(h5f, 'txpath', frequency)
        gain = get_gain(h5f, 'txpath', frequency)
        pae = [p * 100 for p in pae]
        pout = map(sum,zip(pins, gain))
        scatter( pout, pae, color=ELEMENTCOLORS[i])
        xlabel('output power (dBm)')
        ylabel('PAE (%)')
        
        
        subplot(3,1,2)
        scatter(pins, pout, color=ELEMENTCOLORS[i])
        xlabel('input power (dBm)')
        ylabel('output power (dBm)')
        

        subplot(3,1,3)
        freqs = get_freqs(h5f, 'txpath')
        gain = [get_gain(h5f, 'txpath', f)[0] for f in freqs]
        scatter(freqs, gain, color=ELEMENTCOLORS[i])
        xlabel('frequency (Hz)')
        ylabel('gain (dB)')

    legend(TESTELEMENTS)
    show()        
