# jon klein, jtklein@alaska.edu
# jtklein@alaska.edu
# higher level measurement and antenna rotator functions 
# 

import h5py
from vna_control import *

# measures an antenna, saves given tilt, pan, roll, metadata 
def measure_antenna(hd5file, group, suffix, vna, tilt, pan, roll, meastype):
    dsetname =  group + '/t' + str(tilt) + 'p' + str(pan) + 'r' + str(roll) + suffix
    hd5file.create_dataset(dsetname,  data=vna_get_measurement(vna, meastype), compression=DSET_COMPRESSION)
    hd5file[dsetname].attrs.create('roll', roll)
    hd5file[dsetname].attrs.create('tilt', tilt)
    hd5file[dsetname].attrs.create('pan', pan)
    hd5file[dsetname].attrs.create('time', str(time.time()))
    return dsetname

# creates an hdf5 file and prefills frequency vector
def create_h5file(fileprefix, freqs, elements, subgroups): 
    hd5file = h5py.File(fileprefix + time.strftime(FILENAME_DATEFORMAT, time.gmtime())+ FILE_SUFFIX) 
    hd5file.create_dataset('frequencysweep', data=freqs) 
     
    for g in elements: 
        hd5file.create_group(g) 
        for s in subgroups:  
            hd5file.create_group(g + s) 
            hd5file.create_group(g + s) 
            hd5file.create_group(g + s) 
    return hd5file 

# sweeps the antenna through the given pan, tilt, and roll
# measures s21 at each stop and saves results to given hd5file
def sweep_antenna(pans, tilts, rolls, hd5file, vna, name): 
    for t in tilts: 
        servo_setangle(rser, TILT_CHANNEL, t) 
        for p in pans: 
            servo_setangle(rser, PAN_CHANNEL, p) 
            for r in rolls: 
                servo_setangle(rser, ROLL_CHANNEL, r) 
                measure_antenna(hd5file, name, '', vna,  t, p, r, 's21meas') 
 

