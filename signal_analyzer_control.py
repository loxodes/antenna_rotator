# jon klein, jtklein@alaska.edu
# mit license
# library for reading from an Agilent CXA 9000 series signal_analyzer over GPIB
# should work on any PSA, CXA, or ESA series signal analyzer

# adapted from Measurement Guide and Programming Examples PSA and ESA Series Spectrum Analyzers

import visa
from pylab import *

SIGNAL_ANALYZER_ADDR = "GPIB0::18"

def signal_analyzer_init():
    signal_analyzer = visa.instrument(SIGNAL_ANALYZER_ADDR)
    signal_analyzer_preset(signal_analyzer)
    signal_analyzer.write('UNIT:POW DBM')
    signal_analyzer.write('INIT:CONT 0')
    
    return signal_analyzer

def signal_analyzer_readpeak(signal_analyzer, threshold = -70):
    signal_analyzer.write('INIT:IMM;*WAI')
    signal_analyzer.write('CALC:MARK:MAX')
    f = signal_analyzer.ask('CALC:MARK:X?')
    amp = signal_analyzer.ask('CALC:MARK:Y?')
    return {'freq':f,'amp':amp}

def signal_analyzer_readsweep(signal_analyzer):
    signal_analyzer.write('FORM:DATA: REAL,32')
    signal_analyzer.write('INIT:IMM;*WAI')
    vals = signal_analyzer.ask_for_values('TRAC:DATA? TRACE1')
    return vals
    
def signal_analyzer_setref(signal_analyzer, reflevel):
    signal_analyzer.write('DISP:WIND:TRAC:Y:SCAL:RLEV ' + str(reflevel)) 
    
def signal_analyzer_setdiv(signal_analyzer, div):
    signal_analyzer.write('DISP:WIND:TRAC:Y:SCAL:PDIV ' + str(div) + ' dB')
    
def signal_analyzer_setspan(signal_analyzer, span, center, points):
    signal_analyzer.write("SENSe:SWEep:POINts " + str(points))
    signal_analyzer.write("SENSe:FREQuency:CENTer " + str(center) + "e9")
    signal_analyzer.write("SENSe:FREQuency:SPAN " + str(span) + "e9")
 
def signal_analyzer_readspan(signal_analyzer):
    points = int(signal_analyzer.ask("SENSe:SWEep:POINts?"))
    center = float(signal_analyzer.ask("SENSe:FREQuency:CENTer?"))
    span = float(signal_analyzer.ask("SENSe:FREQuency:SPAN?"))
    return linspace(center - span / 2.0, center + span / 2.0, points) * 1e9
  
def signal_analyzer_preset(signal_analyzer):
    signal_analyzer.write("*CLS")
    signal_analyzer.write("*RST")

# example usage: grabs and plots values from signal_analyzer with correct amplitude scaling
if __name__ == "__main__":
    points = 1001
    signal_analyzer = signal_analyzer_init()
    signal_analyzer_setspan(signal_analyzer, 2,2.5,points)
    signal_analyzer_setref(signal_analyzer, 20) # 20 dBm 
    signal_analyzer_setdiv(signal_analyzer, 15) # 15 dB/div
    span = signal_analyzer_readspan(signal_analyzer) 
    print 'peak at: ' + str(signal_analyzer_readpeak(signal_analyzer))
    vals = signal_analyzer_readsweep(signal_analyzer)
    plot(span, vals)
    show()
    
    
