# calculate array factor given:
#   - antenna to antenna spacing
#   - antenna radiation pattern (amplitude?)
#   - phase error
#   - amplitude error
#   - array weighting

# this could be useful for:
# investigating the impact of close up antenna array measurements

# sources:
# Array and Phased Array Antenna Basics. [electronic resource]
# http://catalog.library.uaf.edu/uhtbin/cgisirsi/?ps=yY3n3TEIYy/UAFRAS/263830005/9

# quantization error of linear array with nelements and nbits phase shifters with lspacing wavelength element to element spacing
# see 1.3.5 of Phased Array Antennas Floquet Analysis, Synthesis, BFNs, and Active Array Systems
# assumes uniform array weighting

# all units in mks
# assume perfect polarization...

from pylab import *

PHASE_QUANTIZATION_BITS_DEF = 6

def quantization_error(nelements, nbits, lspacing):
  # calculates quantization error and beam pointing error
  return 20 * log10(((2 ** nbits) / pi) * sin(pi / (2 ** nbits)))

class element:
    def __init__(self, radpat, a, y, z = 0, nbits = PHASE_QUANTIZATION_BITS_DEF):
        self.xpos = x
        self.ypos = y
        self.zpos = z
        self.nbits = nbits
  
        self.radpattern = radpat;
  
    def getField(x, y, z):
        dx = x - self.xpos
        dy = y - self.ypos
        dz = z - self.zpos

        # calculate az angle
        # calculate el angle
        # find radpattern
        # determine phase
        # return complex magnitude from antenna
        # how do I include polarization?

 

# steps:
  # calculate positions of elements
  # calculate weights
  # calculate phase of signals delivered
  # compute array factor
  

