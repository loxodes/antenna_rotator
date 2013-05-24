# jon klein, jtklein@alaska.edu
# mit license
# scripts to characterize an amplifier
# measure
# - P1dB
# - small signal gain
# - current consumption with varying input power level
# - PAE
# -----
# - small and large signal s-parameters 
# and also..
# - characterize attenuator/phase shifters
# save measurements to hdf5 file... structured with:

# array of pin -> pout

from amplifier_measurements import *
from current_measurements import *
from vna_control import *
from hdf5_tools import *
import os

if __name__ == '__main__':
    os.remove('testfile.hdf5')
    h5f = h5py.File('testfile'  + HDF5_SUFFIX)
    h5f.create_group('gain')
    
    freqs = [2.4e9, 2.45e9, 2.5e9] # GHz
    pins = range(-30,7,2)

    sg = siggen_init()
    sa = signal_analyzer_init()
    scope = scope_init()
    
    h5f.create_dataset('gain/pins', data=pins)
    
    # TODO: add calibration of attenuators, constant current draw, etc..
   
    for f in freqs:
        group = 'gain/freq_' + str(f)
        h5f.create_group(group)

        gain = []
        current = []
        
        for p in pins:
            gain.extend([measure_gain(sa, sg, f, p)])
            current.extend([measure_avgcurrent(scope)])
            siggen_rfoff(sg)
        
        h5f.create_dataset(group + '/gain', data=gain) 
        h5f.create_dataset(group + '/current', data=current) 

        # TODO: ADD METADATA TO GAIN AND CURRENT MEASUREMENTS
        # .. attenuation, current measurement tetc..
    
    h5f.close()
