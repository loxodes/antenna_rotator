import h5py
import numpy

GROUP_ATT = '/att_characterization'
GROUP_PHASE = '/phase_characterization'
GROUP_RADPAT = '/pattern_characterization'
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

def get_freqs(hd5filename):
    hd5file = h5py.File(hd5filename, 'r')     
    freqs = hd5file['frequencysweep'][:]
    hd5file.close()
    return freqs

# sorts one array by another array
# this is useful as information in the hdf5 file can get jumbled, and having gain in pan-sorted order is helpful
# http://scienceoss.com/sort-one-list-by-another-list/
def sort_by_array(sortarray, array):
    inds = numpy.argsort(sortarray)
    return numpy.take(array, inds)
