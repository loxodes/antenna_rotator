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

import os, time

def cable_calibrate(h5f, freqs, sa, sg):
    raw_input('bypass DUT and press enter to continue...')
    cal_loss = [0] * len(freqs)
    for (i, f) in enumerate(freqs):
        cal_loss[i] = -measure_gain(sa, sg, f, 0)
        print 'frequency: ' + str(f) + ' cal loss: ' + str(cal_loss[i])
    h5f.create_dataset('calibrated_loss', data=cal_loss)
    raw_input('reconnect DUT and press enter to continue...')
    return cal_loss
    
def measure_lsgain(h5f, groupprefix, freqs, pins,sa, sg, scope, cal_loss, vin = 3.6):
    h5f.create_dataset(groupprefix + '/freqs', data=freqs)
    h5f.create_dataset(groupprefix + '/pins', data=pins)
    
    for (i, f) in enumerate(freqs):
        group = groupprefix + 'gain/freq_' + str(f)
        h5f.create_group(group)
    
        gain = []
        current = []
        pae = []
        
        for p in pins:
            gain.extend([measure_gain(sa, sg, f, p, 20, siggen_disable = False) - cal_loss[i]])
            time.sleep(.01)
            current.extend([measure_avgcurrent(scope)])
            print 'measured current: ' + str(1000*current[-1]) +' mA' 
            pae.extend([(dbm_to_watt(gain[-1]+p)-dbm_to_watt(p))/(vin * current[-1])])
            siggen_rfoff(sg)
        
        h5f.create_dataset(group + '/gain', data=gain) 
        h5f.create_dataset(group + '/current', data=current) 
        h5f.create_dataset(group + '/pae', data=pae)
        
        h5f[group + '/current'].attrs.create('vtoiratio', TRANSCONDUCTANCE_GAIN)
        h5f[group + '/current'].attrs.create('supply_voltage', vin)
    
if __name__ == '__main__':
    os.remove('testfile.hdf5')
    h5f = h5py.File('testfile'  + HDF5_SUFFIX)
    h5f.create_group('gain')
    element = 'f'
    freqs = [2.4e9, 2.45e9, 2.5e9] # GHz
    pins = range(-20,8,3)
    
    
    sg = siggen_init()
    sa = signal_analyzer_init()
    scope = scope_init()
    
    cal_loss = cable_calibrate(freqs, sa, sg)
    measure_lsgain(h5f, 'txpath', freqs, pins, sa, sg, scope, cal_loss)
    
    h5f.close()
