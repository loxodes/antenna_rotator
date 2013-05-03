# jon klein, jtklein@alaska.edu
# mit license
# library for reading s parameters from an Agilent PNA (tested on E8358A)
# sets the center frequency, span, and number of points (requires calibration to be loaded)

import visa
import numpy
import skrf
from pylab import *

VNA_ADDR = "GPIB0::16"
POINTS = 801
F_CENTER = 2.5 # GHz
F_SPAN = 1 # GHz

def vna_init():
    vna = visa.instrument(VNA_ADDR)
    vna.write("INITiate:CONTinuous OFF")
    vna.write("CALCulate:PARameter:DEFine s21meas,S21")
    vna.write("CALCulate:PARameter:DEFine s11meas,S11")
    vna.write("CALCulate:PARameter:DEFine s12meas,S12")
    vna.write("CALCulate:PARameter:DEFine s22meas,S22")
    vna.write("MMEM:STOR:TRAC:FORM:SNP RI") # real/im
    return vna

def vna_get_measurement(vna, measurement_name):
    vna.write("CALCulate:PARameter:SELect " + measurement_name)
    vna.write("INITiate:IMMediate;*wai")
    vals = vna.ask_for_values("CALCulate:DATA? SDATA")
    re = numpy.array([vals[i] for i in range(0,len(vals),2)])
    im = numpy.array([vals[i] for i in range(1,len(vals),2)])
    return re + 1j * im
    
def vna_setspan(vna, span, center, points):
    vna.write("SENSe1:FREQuency:SPAN " + str(span) + "e9")
    vna.write("SENSe1:FREQuency:CENTer " + str(center) + "e9")
    vna.write("SENSe1:SWEep:POINts " + str(points))
    
def vna_readspan(vna):
    points = int(vna.ask("SENSe1:SWEep:POIN?"))
    center = float(vna.ask("SENSe1:FREQuency:CENTer?"))
    span = float(vna.ask("SENSe1:FREQuency:SPAN?"))
    return numpy.linspace(center - span / 2.0, center + span / 2.0, points) * 1e9

def vna_preset(vna):
    vna.write("SYSTem:PRESet;*wai")

# example usage: grabs S21 and S11 from VNA and plots the magnitude and phase
if __name__ == "__main__":
    vna = vna_init()
    vna_setspan(vna, F_SPAN, F_CENTER, POINTS)
    f = vna_readspan(vna)

    # grabs s11 and s21, formatted as complex numbers
    s11 = vna_get_measurement(vna, 's11meas')
    s21 = vna_get_measurement(vna, 's21meas')

    subplot(2,1,1)
    plot(f/1e9, 20*log10(abs(s11)))
    plot(f/1e9, 20*log10(abs(s21)))
    title('amplitude of S11 (blue) and S21 (green)')
    xlabel('frequency (GHz)')
    ylabel('amplitude (dB)')
    xlim([f[0]/1e9, f[-1]/1e9])
    grid(True)

    subplot(2,1,2)
    plot(f/1e9, skrf.complex_2_degree(s11))
    plot(f/1e9, skrf.complex_2_degree(s21))
    title('phase of S11 (blue) and S21 (green)')
    xlabel('frequency (GHz)')
    ylabel('phase (degrees)')
    xlim([f[0]/1e9, f[-1]/1e9])
    grid(True)

    show()
