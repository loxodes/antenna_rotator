# script to plot radiation pattern from anecohic chamber measurements 
from data_processing import *
import array_plot

TESTFILE = 'data/efgh_array.hdf5'
TESTELEMENT = 'steeraz60el40'#'e' + GROUP_RADPAT
TESTFREQ = 2.485 * F_SCALE
TESTROT = 0 

if __name__ == "__main__":
    h5f = h5py.File(TESTFILE, 'r')

    pattern = get_radpattern(h5f, TESTELEMENT, TESTFREQ)
    radarray = get_radarray(pattern) 

#    array_plot.plot_radarray_polar(radarray)
    array_plot.plot_radarraysurf(radarray)
    axis([-90,90,-40,-20])
    prettyify()
    # from radarray, get the equivalent recieved power by a RHCP antenna
    # plot that!
