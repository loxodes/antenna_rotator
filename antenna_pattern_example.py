# example usage of antenna rotator to capture the radiation pattern of a single passive antenna
# jon klein, jtklein@alaska.edu
# mit license
from antenna_pattern import *

# configure sample points for rotator, units are degrees
# each point takes about two seconds, the following scan will take about two hours
AZ_STOPS = range(-80,81,10) # list of azimuth angle stops on for rotator, 0 is boresight (valid range is -90 to +90)
EL_STOPS = range(-10, 71, 10) # list of elevation angle stops for rotator, 0 is level (valid range is +70 to -10)
ROLL_STOPS = range(-180,181,15) # list of roll angle stops for rotator, (valid range is -180 to 180)

if __name__ == "__main__":
    # ask for calibration..    
    raw_input('apply calibration to VNA, and press enter to continue')

    # init VNA
    vna = vna_init()
    f = vna_readspan(vna)

    # init rotator
    rser = serial.Serial(ROTATOR_SERIALPORT, BAUDRATE, timeout=TIMEOUT)
    servo_reset(rser)
   
    # get filename, create hdf5 file
    filename = raw_input('enter a filename: ')
    hd5file = h5py.File(filename + FILE_SUFFIX)

    # save frequency sweep to hdf5 file
    hd5file.create_dataset('frequencysweep', data=f)
    
    # step through specified servo positions, saving S21 to hdf5file at each point
    sweep_antenna(AZ_STOPS, EL_STOPS, ROLL_STOPS, hd5file, vna, rser)   

    # close file and reset positioner to default
    hd5file.close()
    servo_reset(rser)

# to view hdf5 files, see ViTables or HDFView
# parse hdf5 files in python with the h5py library (see data_processing.py for some example code) 
