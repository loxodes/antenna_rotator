# jon klein, jtklein@alaska.edu
# jtklein@alaska.edu

import h5py
from vna_control import *

def measure_antenna(hd5file, group, suffix, vna, tilt, pan, roll, meastype):
    dsetname =  group + '/t' + str(tilt) + 'p' + str(pan) + 'r' + str(roll) + suffix
    hd5file.create_dataset(dsetname,  data=vna_get_measurement(vna, meastype), compression=DSET_COMPRESSION)
    hd5file[dsetname].attrs.create('roll', roll)
    hd5file[dsetname].attrs.create('tilt', tilt)
    hd5file[dsetname].attrs.create('pan', pan)
    hd5file[dsetname].attrs.create('time', str(time.time()))
    return dsetname

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

def sweep_antenna(pans, tilts, rolls, hd5file, vna, name): 
    for t in tilts: 
        servo_setangle(rser, TILT_CHANNEL, t) 
        for p in pans: 
            servo_setangle(rser, PAN_CHANNEL, p) 
            for r in rolls: 
                servo_setangle(rser, ROLL_CHANNEL, r) 
                measure_antenna(hd5file, name, '', vna,  t, p, r) 
 

