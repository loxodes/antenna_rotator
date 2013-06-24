# jon klein, jtklein@alaska.edu
# mit license
# functions to automate characterizing a phased array tr module
# (an sexample of measurement automation using these libraries)

from amplifier_characterize import *
from antenna_pattern import *
import time

TRSTARTUP_DELAY = 4

def measure_phaseatt(h5f, aser, vna, element):
    h5f.create_dataset('vna_frequencysweep', data=vna_readspan(vna))
    h5f.create_group(str(element) + GROUP_ATT)
    h5f.create_group(str(element) + GROUP_PHASE)
    characterize_phaseatt(h5f, vna, element, BASE_ATT, aser)
    
if __name__ == '__main__':
    element = 'g'
    freqs = [2.4e9, 2.45e9, 2.485e9, 2.5e9] # GHz
    txpins = range(-20,5,2)
    rxpins = range(-50,-10, 5)
    vin = 3.6
    cal_loss = [21.562, 21.608, 21.62, 21.714]
    
    h5f = h5py.File('element_' +  element + '_measurements' + str(time.time())[:-3] + HDF5_SUFFIX)  
    aser = serial.Serial(ARRAY_SERIALPORT, BAUDRATE, timeout=TIMEOUT)
    sg = siggen_init()
    sa = signal_analyzer_init()
    scope = scope_init()
    vna = vna_init()
    
    #cable_calibrate(h5f, freqs, sa, sg)
    h5f.create_dataset('calibrated_loss', data=cal_loss)
    
    #raw_input('disconnect power jumper from element, then press enter to continue')
    #disabledcurrent = measure_avgcurrent(scope)
    #h5f.create_dataset('current_measurements/disabledcurrent', data=disabledcurrent)
    #raw_input('reconnect power jumper, then press enter to continue')
    #time.sleep(TRSTARTUP_DELAY)
    
    raw_input('connect amplifier to the VNA, apply calibration, then press enter to continue')
    measure_phaseatt(h5f, aser, vna, element)
    set_mode(aser, element, 'standby')

    raw_input('connect tx path to spectrum analyzer and signal generator, then press enter to continue')
    standbycurrent = measure_avgcurrent(scope)
    h5f.create_dataset('current_measurements/standbycurrent', data=standbycurrent)
    
    set_mode(aser, element, 'tx')
    att_set(aser, element, 0)
    
    measure_lsgain(h5f, 'txpath', freqs, txpins, sa, sg, scope, cal_loss)
    set_mode(aser, element, 'standby')
    
    raw_input('connect rx path to spectrum analyzer and signal generator, then press enter to continue')
    set_mode(aser, element, 'rx')
    rxcurrent = measure_avgcurrent(scope)
    h5f.create_dataset('current_measurements/rxcurrent', data=rxcurrent)
    measure_lsgain(h5f, 'rxpath', freqs, rxpins, sa, sg, scope, cal_loss)
    set_mode(aser, element, 'standby')
   
    h5f.close()