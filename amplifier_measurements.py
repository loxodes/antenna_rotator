# jon klein
# jtklein@alaska.edu, mit license
# functions to automate amplifier measurements

from signal_analyzer_control import *
from siggen_control import *
import time

SPAN_POINTS = 801
SMALL_SIGNAL_LEVEL = -50 # dBm level for small signal gain calculation
REF_LEVEL = 20 # dBm
BANDWIDTH = 1e5 # bandwidth for spectrum analyzer measurements (MHz)
MAX_INPUT = 5 # maximum input (dBm)
AMP_STARTUP = .1 # seconds between siggen enable and measurement

def measure_pxdb(sa, sg, freq, xdb = 1, max_input = MAX_INPUT, ref = REF_LEVEL, bandwidth = BANDWIDTH, startup_delay = AMP_STARTUP):
    small_signal_gain =  measure_gain(sa, sg, freq, SMALL_SIGNAL_LEVEL, ref, bandwidth, startup_delay)
    pxdbin = SMALL_SIGNAL_LEVEL

    for p in range(SMALL_SIGNAL_LEVEL, max_input, .1):
        gain = measure_gain(sa, sg, freq, p, ref, bandwidth, startup_delay)
        if gain < small_signal_gain - xdb:
            break
    
    return pxdbin

def measure_gain(sa, sg, freq, inlevel = SMALL_SIGNAL_LEVEL, ref = REF_LEVEL, bandwidth = BANDWIDTH, startup_delay = AMP_STARTUP, siggen_disable = True, points = SPAN_POINTS):
    siggen_set_amp(sg, inlevel)
    siggen_set_freq(sg, freq)
    siggen_rfon(sg)
    signal_analyzer_setspan(sa, bandwidth, freq, points) 
    signal_analyzer_setref(sa, ref)
    time.sleep(startup_delay)
    peak = signal_analyzer_readpeak(sa)
    gain = peak['amp'] - inlevel
    if siggen_disable:
        siggen_rfoff(sg)
    return gain 

if __name__ == '__main__':
    sg = siggen_init()
    sa = signal_analyzer_init()
    f = 2.45e9 # GHz
    #p1db = measure_pxdb(sa, sg, f)
    for i in range(10):
        gain = measure_gain(sa, sg, f) 
        print 'gain: ' + str(gain)
    
    print 'p1db: ' + str(p1db)


