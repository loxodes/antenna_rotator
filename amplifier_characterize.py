# jon klein, jtklein@alaska.edu
# mit license
# scripts to characterize an amplifier
# measure
# - P1dB
# - small signal gain
# - current consumption with varying input power level
# - PAE
# -----
# - small and large signal s-parameters 
# and also..
# - characterize attenuator/phase shifters
# save measurements to hdf5 file... structured with:

# array of pin -> pout

from amplifier_measurements import *
from vna_control import *
from hdf5tools import *



