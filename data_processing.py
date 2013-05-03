# jon klein, jtklein@alaska.edu
# functions to process data from antenna rotator

from pylab import  *
import h5py, csv

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
# [ theta , re , im ] 
def save_radpattern_csv(pattern, filename):
    with open(filename + '.csv') csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['theta', 'gain_db']
        for i, theta in enumerate(pattern['theta']):
            writer.writerow([theta, pattern['gain'][i])


# quite inefficent.. 
def get_axialratio(hd5file, subgroup, freq, pan, tilt):
    fidx = get_fidx(hd5file, freq)
    max_pos = ''
    max_gain = -inf
    ratio = -inf

    for pos in hd5file[subgroup].keys():
        dset = subgroup + '/' + pos

        if float(hd5file[dset].attrs['pan']) == pan and float(hd5file[dset].attrs['tilt']) == tilt:
            g = 20*log10(abs(hd5file[dset][fidx]))
            if g > max_gain:
                max_pos = float(hd5file[dset].attrs['roll'])
                max_gain = g

    for pos in hd5file[subgroup].keys():
        dset = subgroup + '/' + pos
        if float(hd5file[dset].attrs['pan']) == pan and float(hd5file[dset].attrs['tilt']) == tilt:
            if float(hd5file[dset].attrs['roll']) == (max_pos + 90) or float(hd5file[dset].attrs['roll']) == (max_po
                g = 20*log10(abs(hd5file[dset][fidx]))
                ratio = max_gain - g
                break
    
    return ratio


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

