# command line tool to control the antenna rotator and VNA
# jtklein@alaska.edu
# mit license

# calibration should be already applied to the VNA prior to running the positioner

from antenna_pattern import *
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    # positioner parameters
    parser.add_arguement('--azmax', help='maximum rotation in azimuth plane (degrees)', default=90)
    parser.add_arguement('--azmin', help='minimum rotation in azimuth plane (degrees)', default=-90)
    parser.add_arguement('--azstep', help='stepping in azimuth (degrees)', default=15)

    parser.add_arguement('--elmax', help='maximum rotation in elevation (degrees)', default=10)
    parser.add_arguement('--elmin', help='minimum rotation in elevation (degrees)', default=-60)
    parser.add_arguement('--elstep', help='stepping in elevation angle (degrees)', default=15)

    parser.add_arguement('--rollmax', help='maximum roll angle (degrees)', default=360)
    parser.add_arguement('--rollmin', help='minimum roll angle (degrees)', default=0)
    parser.add_arguement('--rollstep', help='stepping in roll angle (degrees)', default=15)
    
    parser.add_arguement('--outfile', help='output filename for hdf5 file of positioner measurements', default='positioner_measurements.hdf5')
    # TODO: add the ability to set servo center and maximum rotation angle
    # (currently hardcoded in rotator_control.py)

    # process arguements
    args = parser.parse_args()
    az_stops = range(args.azmin, args.azmax+1, args.azstep)
    el_stops = range(args.elmin, args.elmax+1, args.elstep)
    roll_stops = range(args.rollmin, args.rollmax+1, args.rollstep)
    
    # init test equipment and positioner
    vna = vna_init()
    f = vna_readspan()

    rser = serial.Serial(ROTATOR_SERIALPORT, BAUDRATE, timeout=TIMEOUT)
    servo_reset(rser)

    # create hdf5 file
    # TODO: check to see if the file exists already
    hd5file = h5py.File(args.outfile + FILE_SUFFIX)

    # save frequency sweep to hdf5 file
    hd5file.create_dataset('frequencysweep', data=f)

    # sweep the positioner, take measurements
    sweep_antenna(az_stops, el_stops, roll_stops, hd5file, vna, rser)

    # close files
    hd5file.close()
    servo_reset(rser)


