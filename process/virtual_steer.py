# code to predict behavior of steering phased array
# jon klein, jtklein@alaska.edu, mit license

from parse_rotdat import *
from pylab import *
from skrf import * 
import h5py
import cmath
from hdf5_tools import *
import analyze_radpattern
import analyze_phaseatt

ARRAY_SPACING = .45 
HD5FILE = 'ef_arraytest.hdf5'
FREQ = 2.485 * F_SCALE
AZ = 30

def steer_array(hd5file, az, freq, spacing, array):
    dphase = 360 * sin(deg2rad(int(az))) * spacing;
    
    e = analyze_radpattern.get_magphase_pan(hd5file, array[1] + GROUP_RADPAT, freq)
    f = analyze_radpattern.get_magphase_pan(hd5file, array[0] + GROUP_RADPAT, freq)

    theta = e['theta']
    
    e_mag = e['mag']
    f_mag = f['mag']

    f_deg = complex_2_degree(f_mag)
    f_deg = [deg2rad(p + dphase) for p in f_deg]
    f_mag = [complex_2_magnitude(i) for i in f_mag]
    f_mag = [cmath.rect(f_mag[i], f_deg[i]) for i in range(len(f_deg))]
    
    rx = [20*log10(abs(e_mag[i] + f_mag[i])) for i in range(len(theta))]
    
    rx = sort_by_array(theta, rx)
    theta = sort(theta)
    
    return {'theta':theta, 'gain':rx}
        
if  __name__ == '__main__':
    hd5file = h5py.File(HD5FILE, 'r')
    array = ['f', 'e'] # TODO: GET FROM hdf5file (store in metadata!)
    steer = steer_array(hd5file, AZ, FREQ, ARRAY_SPACING, array)
    plot(steer['theta'], steer['gain'])
    show()
