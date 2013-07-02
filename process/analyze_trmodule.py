# extracts spectrum analyzer and signal generator based amplifier measurements from hdf5 file

from pylab import *
from hdf5_tools import *
import h5py
from skrf import complex_2_degree
import pdb

TESTFILE = 'data/g.hdf5'

def get_freqs(h5f, path):
    return h5f[path + '/freqs'][:]

def get_pins(h5f, path):
    return h5f[path + '/pins'][:]

def get_pae(h5f, path, freq):
    return h5f[path + 'gain/freq_' + format(freq) + '/pae'][:]

def get_gain(h5f, path, freq):
    return h5f[path + 'gain/freq_' + format(freq) + '/gain'][:]

def get_current(h5f, path, freq):
    return h5f[path + 'gain/freq_' + format(freq) + '/current'][:]

if __name__ == "__main__":
    h5f = h5py.File(TESTFILE, 'r')
    freqs = get_freqs(h5f, 'txpath')
    get_pins(h5f, 'txpath')
    
    for f in freqs:
        print get_pae(h5f, 'txpath', f)
        print get_gain(h5f, 'txpath', f)
        print get_current(h5f, 'txpath', f)
