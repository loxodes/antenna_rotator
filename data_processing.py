# jon klein, jtklein@alaska.edu
# functions to process data from antenna rotator

from hdf5_tools import *
from pylab import  *
from mlabwrap import mlab
import h5py, csv, os, pdb

def re_to_db(array):
    return [20 * log10(abs(v)) for v in array]


def get_radpattern(hd5file, subgroup, freq, rot):
    fidx = get_fidx(hd5file, freq)

    gain = []
    phi = []
    theta = []

    for pos in hd5file[subgroup].keys():
        dset = subgroup + '/' + pos
        g = 20*log10(abs(hd5file[dset][fidx]))
        t = float(hd5file[dset].attrs['tilt'])
        p = float(hd5file[dset].attrs['pan'])
        r = float(hd5file[dset].attrs['roll'])

        if r == rot:
            phi = phi + [t]
            gain = gain + [g]
            theta = theta + [p]


    gain = sort_by_array(theta,gain)
    phi = sort_by_array(theta,phi)
    theta.sort()
    return {'gain':gain, 'theta':theta, 'phi':phi}

# saves a csv of a radiation pattern
# [ theta , gain] 
def save_radpattern_csv(pattern, filename):
    with open(filename + '.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['theta', 'gain_db'])
        gain = pattern['gain']
        for (i, theta) in enumerate(pattern['theta']):
            writer.writerow([theta, gain[i]])


# calculate axial ratio using MATLAB script from Russel Carroll 
def get_axialratio(hd5file, subgroup, freq, pan, tilt):
    fidx = get_fidx(hd5file, freq)
    slice = get_magphase_roll(hd5file, subgroup, freq, pan, tilt)
    
    mag = [abs(m) for m in slice['mag']]
    roll = [deg2rad(t) for t in slice['roll']]

    mlab.addpath(os.getcwd()) # not a very smart way of doing this
    
    result = mlab.Polarization_Curve_Fit(mag, roll)
    
    emax = result[0][0]
    gamma = result[0][1]
    phi = result[0][2]

    return -20*log10(gamma)

def get_magphase_pan(hd5file, subgroup, freq):
    fidx = get_fidx(hd5file, freq)

    mag = []
    theta = []

    for pos in hd5file[subgroup].keys():
        dset = subgroup + '/' + pos
        m = hd5file[dset][fidx]
        p = float(hd5file[dset].attrs['pan'])

        if r == 0 and t == 0:
            theta = theta + [p]
            mag = mag + [m]

    return {'mag':mag, 'theta':theta}

def get_magphase_roll(hd5file, subgroup, freq, pan, tilt):
    fidx = get_fidx(hd5file, freq)

    roll = []
    mag = []

    for pos in hd5file[subgroup].keys():
        dset = subgroup + '/' + pos
        m = hd5file[dset][fidx]
        r = float(hd5file[dset].attrs['roll'])
        t = float(hd5file[dset].attrs['tilt'])
        p = float(hd5file[dset].attrs['pan'])

        if p == pan and t == tilt:
            roll = roll + [r]
            mag = mag + [m]

    return {'mag':mag, 'roll':roll}


if __name__ == '__main__':
    h5f = h5py.File('e_only.hdf5')
    freqs = get_freqs(h5f)
    
    ax = []
    for f in freqs:
        ax = ax + [get_axialratio(h5f, 'e/pattern_characterization', f, 0, 0)]

    plot(freqs, ax)
    show()
