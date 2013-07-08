# jon klein, jtklein@alaska.edu
# mit license
# functions to automate characterizing a phased array tr module
# (an sexample of measurement automation using these libraries)

from amplifier_characterize import *
from antenna_pattern import *
import time

TRSTARTUP_DELAY = 4

def measure_phaseatt(h5f, aser, vna, element):
    h5f.create_group(str(element) + GROUP_ATT)
    h5f.create_group(str(element) + GROUP_PHASE)
    h5f.create_group(str(element) + GROUP_RAWPHASE)
    h5f.create_group(str(element) + GROUP_RAWATT)
    characterize_phaseatt(h5f, vna, element, 0, aser)
    
if __name__ == '__main__':
    elements = ['e', 'f', 'g', 'h']
    freqs = [2.4e9, 2.45e9, 2.485e9, 2.5e9] # GHz
    txpins = range(-20,7,2)
    rxpins = range(-50,0, 5)
    vin = 3.6
    cal_loss = [21.562, 21.608, 21.62, 21.714]
    
    h5f = h5py.File('elements_' +  ''.join(elements) + '' + str(time.time())[:-3] + HDF5_SUFFIX)  
    aser = serial.Serial(ARRAY_SERIALPORT, BAUDRATE, timeout=TIMEOUT)
    #sg = siggen_init()
    #sa = signal_analyzer_init()
    #scope = scope_init()
    vna = vna_init()
    
    #cable_calibrate(h5f, freqs, sa, sg)
    h5f.create_dataset('calibrated_loss', data=cal_loss)
    
    #raw_input('disconnect power jumper from element, then press enter to continue')
    #disabledcurrent = measure_avgcurrent(scope)
    #h5f.create_dataset('current_measurements/disabledcurrent', data=disabledcurrent)
    #raw_input('reconnect power jumper, then press enter to continue')
    #time.sleep(TRSTARTUP_DELAY)
    
  #  for e in elements:
        #raw_input('connect element ' +  e + ' tx path to spectrum analyzer and signal generator, then press enter to continue')
        #standbycurrent = measure_avgcurrent(scope)
        #h5f.create_dataset(e + '/current_measurements/standbycurrent', data=standbycurrent)
          
        #set_mode(aser, e, 'tx')
        #att_set(aser, e, 0)
        
        #measure_lsgain(h5f, e + '/txpath', freqs, txpins, sa, sg, scope, cal_loss)
        #set_mode(aser, e, 'standby')
        
        #raw_input('connect rx path to spectrum analyzer and signal generator, then press enter to continue')
        #set_mode(aser, e, 'rx')
        #rxcurrent = measure_avgcurrent(scope)
       # h5f.create_dataset(e + '/current_measurements/rxcurrent', data=rxcurrent)
        #measure_lsgain(h5f, e + '/rxpath', freqs, rxpins, sa, sg, scope, cal_loss)
       # set_mode(aser, e, 'standby')
        
    for e in elements:
        raw_input('connect element ' + str(e) + ' transmit path to the VNA, apply calibration, then press enter to continue')
        measure_phaseatt(h5f, aser, vna, e)
        set_mode(aser, e, 'standby')
        
    h5f.create_dataset('vna_frequencysweep', data=vna_readspan(vna))
    h5f.close()