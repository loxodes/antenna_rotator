# jon klein, jtklein@alaska.edu
# functions to process data from antenna rotator

from hdf5_tools import *
from pylab import  *
#from mlabwrap import mlab
import h5py, csv, os
import pdb

# convert a voltage to dB
def re_to_db(array):
    return [20 * log10(abs(v)) for v in array]

# dumps a 1d list of gain, magnitude, theta, phi, and rotation given a group and frequency
def get_radpattern(hd5file, subgroup, freq):
    fidx = get_fidx(hd5file, freq)

    gain = np.array([])
    phi = np.array([])
    theta = np.array([])
    mag = np.array([])
    rot = np.array([])
    print subgroup 
    for pos in hd5file[subgroup].keys():
        dset = subgroup + '/' + pos

        gain = np.append(20*log10(abs(hd5file[dset][fidx])), gain)
        mag = np.append(hd5file[dset][fidx], mag)
        theta = np.append(float(hd5file[dset].attrs['pan']), theta)
        phi = np.append(float(hd5file[dset].attrs['tilt']), phi)
        rot = np.append(float(hd5file[dset].attrs['roll']), rot)

    return {'gain':gain, 'theta':theta, 'phi':phi, 'rot':rot, 'mag':mag}

# converts the 1d gain and magnitude list into a 3d array as a function of theta, phi, and roll
def get_radarray(pattern):
    thetas = sort(list(set(pattern['theta'])))
    rots = sort(list(set(pattern['rot'])))
    phis = sort(list(set(pattern['phi'])))
    
    radarray_gain = np.zeros([len(thetas), len(phis), len(rots)])
    radarray_mag = np.zeros([len(thetas), len(phis), len(rots)])

    az = pattern['theta']
    el = pattern['phi']
    rot = pattern['rot']
    gain = pattern['gain']
    mag = pattern['mag']
    

    # instead...
    # get axial ratio and equivalent received path loss by a perfect circularlly polarized antenna

    for i in range(len(az)):
        radarray_gain[numpy.where(thetas == az[i]),numpy.where(phis == el[i]),numpy.where(rots == rot[i])] = gain[i]
        radarray_mag[numpy.where(thetas == az[i]),numpy.where(phis == el[i]),numpy.where(rots == rot[i])] = mag[i]

    return {'radarray_gain':radarray_gain, 'radarray_mag':radarray_mag, 'thetas':thetas, 'phis':phis, 'rots':rots}

# return 2d table of elevation/azimuth steering
def get_steertable(hd5file):
    azsteers = []
    elsteers = []
    for dset in hd5file.items():
        if dset[0][0:5] == 'steer':
            vnasweep = hd5file[dset[0] + '/' + hd5file[dset[0]].items()[0][0]]
            elsteers.append(int(vnasweep.attrs['elsteer']))
            azsteers.append(int(vnasweep.attrs['azsteer']))
    
    azsteers = sort(list(set(azsteers)))
    elsteers = sort(list(set(elsteers)))
    return meshgrid(azsteers, elsteers)


# gets the gain of the array compared to a single element
def get_arraygain(hd5file, freq, omnielement, azrange, elrange):
    omnipattern = get_radarray(get_radpattern(hd5file, omnielement, freq))
   
    arraygain = zeros([len(elrange), len(azrange)])

    for (i,az) in enumerate(azrange):
        for (j,el) in enumerate(elrange): 
            array = get_radarray(get_radpattern(hd5file, 'steeraz' + str(az) + 'el' + str(el), freq))
            
            azidx = numpy.where(array['thetas'] == az)[0][0]
            elidx = numpy.where(array['phis'] == el)[0][0]
            
            arraygain[j,i] = max(array['radarray_gain'][azidx,elidx]) - max(omnipattern['radarray_gain'][azidx, elidx])

    return arraygain
    

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
    h5f = h5py.File('data/efgh_array.hdf5')
    omnielement = 'g/pattern_characterization'
    arraygain = get_arraygain(h5f, 2.485e18, omnielement, range(-60,61,20), range(0,61,20))
