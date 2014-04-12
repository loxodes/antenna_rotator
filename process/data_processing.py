# jon klein, jtklein@alaska.edu
# functions to process data from antenna rotator

from hdf5_tools import *
from pylab import  *
from ellipse_tools import *
import h5py, csv, os, cmath
import pdb

def prettyify():
    matplotlib.rcParams.update({'font.size': 23})
    matplotlib.rcParams.update({'font.weight': 'bold'})
    matplotlib.rcParams.update({'legend.loc': 'best'})
    grid(True)
    legend(fancybox=True)

# convert a voltage to dB
def re_to_db(array):
    return [20 * log10(abs(v)) for v in array]

def db_to_re(array, mult=20):
    v = np.vectorize(_db_to_re)
    return v(array)

def _db_to_re(v, mult=20):
    return pow(10, v/mult)

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
    
    radarray_gain =  np.zeros([len(thetas), len(phis), len(rots)])
    radarray_mag = (1j + 1) * np.zeros([len(thetas), len(phis), len(rots)])

    az = pattern['theta']
    el = pattern['phi']
    rot = pattern['rot']
    gain = pattern['gain']
    mag = pattern['mag']
    

    # instead...
    # get axial ratio and equivalent received path loss by a perfect circularlly polarized antenna

    for i in range(len(az)):
        radarray_gain[numpy.where(thetas == az[i]), numpy.where(phis == el[i]), numpy.where(rots == rot[i])] = gain[i]
        radarray_mag[numpy.where(thetas == az[i]), numpy.where(phis == el[i]), numpy.where(rots == rot[i])] = mag[i]

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

# return a 2d table of az/el rot 
def get_rottable(hd5file):
    azsteers = []
    elsteers = []
    rollsteers = []

    for dset in hd5file.items():
        if dset[0][0:5] == 'steer':
            for steering in dset[1].items():
                elsteers.append(int(steering[1].attrs['tilt']))
                azsteers.append(int(steering[1].attrs['pan']))
                rollsteers.append(int(steering[1].attrs['roll']))
            break 

    azsteers = sort(list(set(azsteers)))
    elsteers = sort(list(set(elsteers)))
    rollsteers = sort(list(set(rollsteers)))
    return {'azsteers':azsteers, 'elsteers':elsteers, 'rollsteers':rollsteers} 



# gets the gain of the array compared to the average of all individual elements
def get_arraygain(hd5file_array, hd5file_omni, freq, omnielement, azrange, elrange, elementprefix = '/pattern_characterization', gain = 1):
    omnipattern = get_radarray(get_radpattern(hd5file_omni, omnielement + elementprefix, freq))
    arraygain = zeros([len(elrange), len(azrange)])

    for (i,az) in enumerate(azrange):
        for (j,el) in enumerate(elrange): 
            array = get_radarray(get_radpattern(hd5file_array, 'steeraz' + str(az) + 'el' + str(el), freq))
            
            azidx_array = numpy.where(array['thetas'] == az)[0][0]
            elidx_array = numpy.where(array['phis'] == el)[0][0]

            azidx_omni = numpy.where(omnipattern['thetas'] == az)[0][0]
            elidx_omni = numpy.where(omnipattern['phis'] == el)[0][0]

            ax_array = get_axialratio(array['rots'], array['radarray_mag'][azidx_array,elidx_array])
            ax_omni = get_axialratio(omnipattern['rots'], omnipattern['radarray_mag'][azidx_omni,elidx_omni])

            arraygain[j,i] = ax_array['directivity'] - ax_omni['directivity']  * gain
    return arraygain

# shifts a complex magnitude by phase radians 
def shift_mag(cmag, phase):
    (r, phi) = cmath.polar(cmag)
    return cmath.rect(r, phi + phase)
    


# calculates the expected radiation pattern of an array using the measured pattern from one element 
def calc_arraygain(hd5file_omni, freq, omnielement, azrange, elrange, rotrange, azsteer, elsteer, offset, dx = .47, dy = .47, N=2, M=2, elementprefix = '/pattern_characterization'):
    # create array of S21 magnitude [el, az, roll]
    omnipattern = get_radarray(get_radpattern(hd5file_omni, omnielement, freq))
    omnimag = (1 + 1j) * zeros([len(elrange), len(azrange), len(rotrange)])
    for (i,az) in enumerate(azrange):
        for (j,el) in enumerate(elrange):
            for(k, rot) in enumerate(rotrange):
                    azidx_omni = numpy.where(omnipattern['thetas'] == az)[0][0]
                    elidx_omni = numpy.where(omnipattern['phis'] == el)[0][0]
                    rotidx_omni = numpy.where(omnipattern['rots'] == rot)[0][0]
                    omnimag[j,i,k] = omnipattern['radarray_mag'][azidx_omni,elidx_omni,rotidx_omni]
    
    # create an array with the sum of the complex magnitude for each element
    l = 3e8 / (freq/1e9)
    dazphase = 2 * pi * sin(deg2rad(azsteer)) * (dx)
    delphase = 2 * pi * sin(deg2rad(elsteer)) * (dy) 

    arraypattern = (1 + 1j) * zeros([len(elrange), len(azrange), len(rotrange)])
    arrayrhcp  = (1 + 1j) * zeros([len(elrange), len(azrange)])
    for (i,az) in enumerate(azrange):
        for (j,el) in enumerate(elrange):
            for(k, rot) in enumerate(rotrange):
                cmag = omnimag[j,i,k]
                amag = 0

                # add phase shift for steering
                for n in range(N):
                    for m in range(M):
                        azweight = n * 2 * pi * sin(deg2rad(az)) * (dx)
                        elweight = m * 2 * pi * sin(deg2rad(el)) * (dy)
                        tmag = shift_mag(cmag, m * delphase + n * dazphase + azweight + elweight)
                        amag += tmag

                arraypattern[j,i,k] = amag
            arrayrhcp[j,i] = get_axialratio(rotrange,arraypattern[j,i,:])['directivity'] + offset 
    return {'radarray_mag':arraypattern, 'thetas':azrange, 'phis':elrange, 'rots':rotrange,'rhcppattern':arrayrhcp}

# calculates the expected radiation pattern of an array using the measured pattern from one element 
def calc_maxarraygain(hd5file_omni, freq, omnielement, azrange, elrange, rotrange, azsteer, elsteer, offset, dx = .47, dy = .47, N=2, M=2, elementprefix = '/pattern_characterization'):
    # create array of S21 magnitude [el, az, roll]
    omnipattern = get_radarray(get_radpattern(hd5file_omni, omnielement, freq))
    omnimag = (1 + 1j) * zeros([len(elrange), len(azrange), len(rotrange)])
    for (i,az) in enumerate(azrange):
        for (j,el) in enumerate(elrange):
            for(k, rot) in enumerate(rotrange):
                    azidx_omni = numpy.where(omnipattern['thetas'] == az)[0][0]
                    elidx_omni = numpy.where(omnipattern['phis'] == el)[0][0]
                    rotidx_omni = numpy.where(omnipattern['rots'] == rot)[0][0]
                    omnimag[j,i,k] = omnipattern['radarray_mag'][azidx_omni,elidx_omni,rotidx_omni]
    
    # create an array with the sum of the complex magnitude for each element
    l = 3e8 / (freq/1e9)
    arraypattern = (1 + 1j) * zeros([len(elrange), len(azrange), len(rotrange)])
    arrayrhcp  = (1 + 1j) * zeros([len(elrange), len(azrange)])
    for (i,az) in enumerate(azrange):
        for (j,el) in enumerate(elrange):
            dazphase = 2 * pi * sin(deg2rad(-az)) * (dx)
            delphase = 2 * pi * sin(deg2rad(-el)) * (dy) 

            for(k, rot) in enumerate(rotrange):
                cmag = omnimag[j,i,k]
                amag = 0

                # add phase shift for steering
                for n in range(N):
                    for m in range(M):
                        azweight = n * 2 * pi * sin(deg2rad(az)) * (dx)
                        elweight = m * 2 * pi * sin(deg2rad(el)) * (dy)
                        tmag = shift_mag(cmag, m * delphase + n * dazphase + azweight + elweight)
                        amag += tmag

                arraypattern[j,i,k] = amag
            arrayrhcp[j,i] = get_axialratio(rotrange,arraypattern[j,i,:])['directivity'] + offset 
    return {'radarray_mag':arraypattern, 'thetas':azrange, 'phis':elrange, 'rots':rotrange,'rhcppattern':arrayrhcp}


# calculates path loss adjustment between a single element and a N by M element array to compensate for increased transmit power and element overhead
def calc_dploss(N, M, Ptot, Pelem):
    return 10 * log10(N * M) - 10 * log10((Ptot - (N * M) * Pelem)/Ptot)

# saves a csv of a radiation pattern
# [ theta , gain] 
def save_radpattern_csv(pattern, filename):
    with open(filename + '.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['theta', 'gain_db'])
        gain = pattern['gain']
        for (i, theta) in enumerate(pattern['theta']):
            writer.writerow([theta, gain[i]])


# calculate axial ratio and recieved power by 
def get_axialratio(roll, mag):
    mag = [abs(m) for m in mag] 
    roll = [deg2rad(r) for r in roll] 
    
    points = [cmath.rect(mag[i], roll[i]) for i in range(len(roll))]

    a = fit_ellipse(real(points), imag(points))
    axis_lengths = ellipse_axis_length(a)
    
    axialratio = abs(20 * log10(axis_lengths[0] / axis_lengths[1]))
    directivity = 20 * log10(axis_lengths[0] + axis_lengths[1]) + get_mismatch_loss(axialratio)
    return {'axialratio':axialratio, 'directivity':directivity}

def get_mismatch_loss(axialratio):
    # axialratio is in dB
    # calculate mismatch loss from a circularly polarized antenna
    # see polarization mismatch loss equation from: http://www.cobham.com/media/83787/805-1.pdf 
    yc = 1
    ye = pow(10, axialratio / 10.0) 
    mismatch_loss = 10 * log10(.5 + .5 * ((2 * yc * ye) / (1 + ye * ye)))
    return mismatch_loss

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
    h5f_array = h5py.File('data/efgh_steerpoint_element_2p485ghz_13_11_02_21_13.hdf5')
    h5f_omni = h5py.File('data/g_element_2p485ghz_13_10_27_02_55.hdf5')
    omnielements = ['g']
    arraygains = []
    arraygains = get_arraygain(h5f_array, h5f_omni, 2.485e18, omnielements[0], range(-90,91,10), range(0,61,10))
    imshow(arraygains)
    show()
    #arraygains = minimum(minimum(arraygains[0], arraygains[1]), minimum(arraygains[2], arraygains[2]))
    #gain_avg = 20*log10(arraygains)

    print arraygains 
