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
# from antenna_pattern import *
import os

if __name__ == '__main__':
    os.remove('testfile.hdf5')
    h5f = h5py.File('testfile'  + HDF5_SUFFIX)
    h5f.create_group('gain')
    element = 'f'
    freqs = [2.4e9, 2.45e9, 2.5e9] # GHz
    pins = range(-30,7,2)
    vin = 3.6
    
    sg = siggen_init()
    sa = signal_analyzer_init()
    scope = scope_init()
    
    calresponse = raw_input('if you want to calibrate out attenuators and cables, bypass the amplifier and connect them between the signal generator and signal analyzer and enter y. otherwise, type n: ').lower()
    cal_loss = [0] * len(freqs)
    if(calresponse[0].lower() == 'y'): 
        for (i, f) in enumerate(freqs):
            cal_loss[i] = -measure_gain(sa, sg, f, 0)
        raw_input('connect your amplifier and press enter to continue...')
        h5f.create_dataset('calibrated_loss', data=cal_loss)
        
    h5f.create_dataset('gain/pins', data=pins)    
    h5f.create_dataset('gain/freqs', data=freqs)  
    
    for (i, f) in enumerate(freqs):
        group = 'gain/freq_' + str(f)
        h5f.create_group(group)

        gain = []
        current = []
        pae = []
        
        for p in pins:
            gain.extend([measure_gain(sa, sg, f, p) + cal_loss[i]])
            current.extend([measure_avgcurrent(scope)])
            pae.extend([(dbm_to_watt(gain[-1]+p)-dbm_to_watt(p))/(vin * current[-1])])
            siggen_rfoff(sg)
        
        h5f.create_dataset(group + '/gain', data=gain) 
        h5f.create_dataset(group + '/current', data=current) 
        h5f.create_dataset(group + '/pae', data=pae)
        
        hd5file[group + '/current'].attrs.create('vtoiratio', TRANSCONDUCTANCE_GAIN)
        hd5file[group + '/current'].attrs.create('supply_voltage', vin)
        
    
#    raw_input('connect amplifier to the VNA, apply calibration, then press enter to continue')
#    vna = vna_init()
#    hd5file.create_dataset('vna_frequencysweep', data=vna_readspan(vna))
#    hd5file.create_group(str(element) + GROUP_ATT)
#    hd5file.create_group(str(element) + GROUP_PHASE)
#    hd5file.create_group(str(element) + GROUP_RADPAT)
#    aser = serial.Serial(ARRAY_SERIALPORT, BAUDRATE, timeout=TIMEOUT)
#    characterize_phaseatt(hd5file, vna, element, BASE_ATT, aser)
    
    h5f.close()
