# jon klein, jtklein@alaska.edu
# functions to process data from antenna rotator

from hdf5_tools import *
from pylab import  *
#from mlabwrap import mlab
import h5py, csv, os
import pdb

def re_to_db(array):
    return [20 * log10(abs(v)) for v in array]


def get_radpattern(hd5file, subgroup, freq):
    fidx = get_fidx(hd5file, freq)

    gain = np.array([])
    phi = np.array([])
    theta = np.array([])
    mag = np.array([])
    rot = np.array([])

    for pos in hd5file[subgroup].keys():
        dset = subgroup + '/' + pos

        gain = np.append(20*log10(abs(hd5file[dset][fidx])), gain)
        mag = np.append(hd5file[dset][fidx], mag)
        theta = np.append(float(hd5file[dset].attrs['pan']), theta)
        phi = np.append(float(hd5file[dset].attrs['tilt']), phi)
        rot = np.append(float(hd5file[dset].attrs['roll']), rot)

#    gain = sort_by_array(theta,gain)
#    phi = sort_by_array(theta,phi)
#    theta.sort()
    return {'gain':gain, 'theta':theta, 'phi':phi, 'rot':rot, 'mag':mag}

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

#    mlab.addpath(os.getcwd()) # not a very smart way of doing this
    
#    result = mlab.Polarization_Curve_Fit(mag, roll)
    
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
    mag = sort_by_array(theta, mag)
    theta.sort()
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
