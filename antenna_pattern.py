# jon klein, jtklein@alaska.edu
# mit license
# creates calibration table for nshifter channel

from pylab import *
from vna_control import *
from retro_control import *
from rotator_control import *
import skrf, time, pdb, h5py

FILENAMEPREIX = 'e_only_arraytest'
FILENAME_DATEFORMAT = '_%y_%m_%d_%H_%M' # append date to filenames, see http://docs.python.org/2/library/time.html

VNA_CALNAME = 'INSERT CALIBRATION HERE INFORMATION HERE'
DSET_COMPRESSION = 'lzf'

GROUP_ATT = '/att_characterization'
GROUP_PHASE = '/phase_characterization'
GROUP_RADPAT = '/pattern_characterization'
FILE_SUFFIX = '.hdf5'
GROUP_STEER = '/steer'
#ELEMENTS = ['e', 'f']
ELEMENTS = ['e']
ARRAY_SERIALPORT = 'COM8'
ROTATOR_SERIALPORT = 'COM9'
BAUDRATE = 9600
TIMEOUT = 1
TX_STARTUP = .1
PAN_STOPS = range(-80,80,10)
TILT_STOPS = [0]
ROLL_STOPS = [0] #range(-180,181,45)

ARRAY_STEERS = range(-90,90,10)

BASE_ATT = 8
BASE_PHASE = 0

def get_phase(vna, meas):
    time.sleep(.01)
    s = vna_get_measurement(vna, meas)
    return skrf.complex_2_degree(s)

def get_atten(vna, meas):
    time.sleep(.01)
    s = vna_get_measurement(vna, meas)
    return 20 * log10(abs(s))    

def sweep_elements(pans, tilts, rolls, hd5file, vna, elements, rser, aser, steers):
    for t in tilts:
        servo_setangle(rser, TILT_CHANNEL, t)
        for p in pans:
            servo_setangle(rser, PAN_CHANNEL, p)
            for r in rolls:
                servo_setangle(rser, ROLL_CHANNEL, r)
                time.sleep(4)
                print 'measuring pan ' + str(p) + ' tilt ' + str(t) + ' roll ' + str(r)
                measure_elements(hd5file, GROUP_RADPAT, vna, elements, aser, t, p, r, BASE_ATT, BASE_PHASE)
                #for s in steers:
                #    print 'measuring steer ' + str(s)
                #    measure_sweep(hd5file, GROUP_STEER, vna, t, p, r, s, elements, aser)
                    
def sweep_antenna(pans, tilts, rolls, hd5file, vna):
    for t in tilts:
        servo_setangle(rser, TILT_CHANNEL, t)
        for p in pans:
            servo_setangle(rser, PAN_CHANNEL, p)
            for r in rolls:
                servo_setangle(rser, ROLL_CHANNEL, r)
                measure_antenna(hd5file, 'antenna_test', '', vna,  t, p, r)


def characterize_phaseatt(hd5file, vna, elements, baseatt, ser):
    print 'characterizing element phase'
    # set all to standby except element, set element to tx
    att = baseatt

    for phase in range(0,380,5):
        print 'measuring phase shift ' + str(phase)
        measure_elements(hd5file, GROUP_PHASE, vna, elements, ser, 0, 0, 0, att, phase)
            
    print 'characterizing element attenuation'
    for att in range(16):
        print 'measuring attenuation setting ' + str(att)
        measure_elements(hd5file, GROUP_ATT, vna, elements, ser, 0, 0, 0, att, 0)
   
def measure_elements(hd5file, group, vna, elements, ser, tilt, pan, roll, att, phase):
    # set all to standby, att0, phase0
    for e in elements:
        time.sleep(.1)
        print 'measuring element ' + e
        for el in elements:
            set_mode(ser, el, 'standby')
        
        att_set(ser, e, att)
        att_set(ser, e, att)
        phase_set(ser, e, phase)
        
        set_mode(ser, e, 'tx')
        time.sleep(TX_STARTUP) 
        suffix = 'att' + str(att) + 'phase' + str(phase)
        dsetname = measure_antenna(hd5file, e + group, suffix, vna, tilt, pan, roll)
        set_mode(ser, e, 'standby')
        hd5file[dsetname].attrs.create('elements', str(elements)) 
        hd5file[dsetname].attrs.create('att', str(att)) 
        hd5file[dsetname].attrs.create('phase', str(phase))


def measure_sweep(hd5file, group, vna, tilt, pan, roll,steer, elements, ser):
    for e in elements:
        set_mode(aser, e, 'tx')
        att_set(ser, e, BASE_ATT)
        
    time.sleep(TX_STARTUP)   
    
    array_steer(aser, steer, 0)
    dsetname = measure_antenna(hd5file, group + str(steer), '', vna, tilt, pan, roll)
    hd5file[dsetname].attrs.create('elements', str(elements)) 
    hd5file[dsetname].attrs.create('steer', str(steer))
    for e in elements:
        set_mode(aser, e, 'standby')

def measure_antenna(hd5file, group, suffix, vna, tilt, pan, roll):
    dsetname =  group + '/t' + str(tilt) + 'p' + str(pan) + 'r' + str(roll) + suffix
    hd5file.create_dataset(dsetname,  data=vna_get_measurement(vna,'s21meas'))#, compression=DSET_COMPRESSION)
    hd5file[dsetname].attrs.create('roll', roll)
    hd5file[dsetname].attrs.create('tilt', tilt)
    hd5file[dsetname].attrs.create('pan', pan)
    hd5file[dsetname].attrs.create('time', str(time.time()))
    return dsetname

def create_h5file(fileprefix, freqs, elements, steering):
    hd5file = h5py.File(fileprefix + time.strftime(FILENAME_DATEFORMAT, time.gmtime())+ FILE_SUFFIX)
    hd5file.create_dataset('frequencysweep', data=freqs)

    for g in elements:
        hd5file.create_group(g)
        hd5file.create_group(g + GROUP_ATT)
        hd5file.create_group(g + GROUP_PHASE)
        hd5file.create_group(g + GROUP_RADPAT)
    
    for s in steering:
        hd5file.create_group(GROUP_STEER + str(s))
        
    return hd5file
    

if __name__ == "__main__":
    # init VNA
    vna = vna_init()
    f = vna_readspan(vna)
    
    # init array
    aser = serial.Serial(ARRAY_SERIALPORT, BAUDRATE, timeout=TIMEOUT)
    
    # init rotator
    rser = serial.Serial(ROTATOR_SERIALPORT, BAUDRATE, timeout=TIMEOUT)
    servo_setspeed(rser, ROLL_CHANNEL, 10)
    servo_setspeed(rser, PAN_CHANNEL, 10)
    servo_reset(rser)    
    
    # create hd5f file
    hd5file = create_h5file(FILENAMEPREIX, f, ELEMENTS, ARRAY_STEERS)
    
    print 'init complete'
    # sweep antenna
    #sweep_antenna(PAN_STOPS, TILT_STOPS, ROLL_STOPS, hd5file, vna)
    
    print 'characterizing phase and attenuation'
    # measure individual element phase and attenuation variations
    #characterize_phaseatt(hd5file, vna, ELEMENTS, BASE_ATT, aser)

    # sweep each element, measure phase s21 at each stop
    sweep_elements(PAN_STOPS, TILT_STOPS, ROLL_STOPS, hd5file, vna, ELEMENTS, rser, aser, ARRAY_STEERS)
    
    hd5file.close()
