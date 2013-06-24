# jon klein, jtklein@alaska.edu
# mit license
# library for controlling  Agilent E4000 series signal generator (tested on an E4433B)

import visa, time
from pylab import *

SIGGEN_ADDR = "GPIB0::19"
SIGGEN_DELAY = .1 # delay after signal generator setting.

def siggen_init():
    siggen = visa.instrument(SIGGEN_ADDR)
    siggen_preset(siggen)
    siggen_rfoff(siggen)
    return siggen

def siggen_set_freq(siggen, freq):
    siggen.write(':FREQ ' + str(freq) + ' Hz')
    
def siggen_set_amp(siggen, amp):
    siggen.write('POW:AMPL ' + str(amp) + ' dBm')
    
def siggen_rfon(siggen):
    siggen.write('OUTP:STAT ON')
    
def siggen_rfoff(siggen):
    siggen.write('OUTP:STAT OFF')
 
def siggen_preset(siggen):
    siggen.write("*RST")

# example usage: sets the frequency and amplitude of the signal generator
if __name__ == "__main__":
    siggen = siggen_init()
    siggen_set_freq(siggen, 1.2345e9)
    siggen_set_amp(siggen, -10)
    siggen_rfon(siggen)
    
