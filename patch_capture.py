# jon klein, jtklein@alaska.edu
# mit license
# measures s11 and E and H radiation pattern at resonance of patch antenna 

from pylab import *
from vna_control import *
from rotator_control import *
from sweep_control import *
from data_processing import *
import skrf, time, pdb, h5py

FILENAMEPREIX = 'antenna_test'
FILENAME_DATEFORMAT = '_%y_%m_%d_%H_%M' # append date to filenames, see http://docs.python.org/2/library/time.html

VNA_CALNAME = ''
DSET_COMPRESSION = 'lzf'

GROUP_S11= '/s11'
GROUP_S21= '/s21'

FILE_SUFFIX = '.hdf5'

ROTATOR_SERIALPORT = 'COM9'
BAUDRATE = 9600
TIMEOUT = 1

PAN_STOPS = range(-90,90,5)
TILT_STOPS = [0]
ROLL_STOPS = [0, 90] 

BASE_ATT = 8
BASE_PHASE = 0
 
if __name__ == "__main__":
    # init VNA
    vna = vna_init()
    f = vna_readspan(vna)
    
    # init rotator
    rser = serial.Serial(ROTATOR_SERIALPORT, BAUDRATE, timeout=TIMEOUT)
    servo_reset(rser)    
   
    # create hd5f file
    hd5file = create_h5file('array', f, ELEMENTS)
   
    # measure s11 at boresight
    print 'init complete, measuring S11'
    measure_antenna(hd5file, GROUP_S11, '', vna, 0, 0, 0, 's11meas')

    # measure s21
    sweep_antenna(PAN_STOPS, TILT_STOPS, ROLL_STOPS, hd5file, vna, GROUP_S21)
    print 'sweeping array to find radiation pattern'

    # find index of resonant frequency of s11 
    s11 = re_to_db(hd5file[GROUP_S11])
    s11_minidx = s11.index(min(s11))
    f_center = hd5file['freqs'][s11_minidx]
    
    # plot radiation pattern at this frequency for E and H
    e_pattern = get_radpattern(hd5file, GROUP_S21, f_center, 0)
    h_pattern = get_radpattern(hd5file, GROUP_S21, f_center, 90)

    plot(e_pattern['theta'],e_pattern['gain'])
    plot(h_pattern['theta'],h_pattern['gain'])

    pdb.set_trace() 
    hd5file.close()
    print 'characterizing phase and attenuation'
    # measure individual element phase and attenuation variations
    
