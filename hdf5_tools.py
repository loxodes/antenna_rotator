# jon klein, jtklein@alaska.edu
# mit license

import h5py
import numpy
from pylab import *

HDF5_SUFFIX = '.hdf5'
DSET_COMPRESSION = '.lzf'
F_SCALE = 1e18

# gets the index of a frequency closed to one from an hdf5 file
def get_fidx(hd5file, freq):
    if freq < hd5file['frequencysweep'][0] or freq > hd5file['frequencysweep'][-1]:
        print 'error: frequency ' + str(freq) + ' is out the bounds of the sweep.. defaulting to first frequency'
        fidx = 0
    else:
        npts = len(hd5file['frequencysweep'])
        df = hd5file['frequencysweep'][1] -  hd5file['frequencysweep'][0]
        fidx = int((freq - hd5file['frequencysweep'][0])/df)

    return fidx

def get_freqs(hd5file):
    freqs = hd5file['frequencysweep'][:]
    return freqs

# sorts one array by another array
# this is useful as information in the hdf5 file can get jumbled, and having gain in pan-sorted order is helpful
# http://scienceoss.com/sort-one-list-by-another-list/
def sort_by_array(sortarray, array):
    inds = numpy.argsort(sortarray)
    return numpy.take(array, inds)

def export_touchstone_s1p(hd5file, group, filename):
    s1pfile = open(filename + '.s1p', 'w')

    s11 = hd5file[group][:]

    s1pfile.write('! s1p file attempt\n')
    
    s1pfile.write('# HZ S RI R 50\n')
    s1pfile.write('! freq re(s11) im(s11)\n')
    freqs = get_freqs(hd5file)
    for i, f in enumerate(freqs):
        s1pfile.write(str(f/1e9) + '\t' + str(real(s11[i])) + '\t' + str(imag(s11[i])) + '\n')
    
    s1pfile.close()
