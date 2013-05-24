# jon klein, jtklein@alaska.edu
# mit license
# library for reading from an Agilent 54620 series scope (tested on 54621A)

import visa
from pylab import *

SCOPE_ADDR = "GPIB0::7"
CURRENT_RESISTOR

def scope_init():
    scope = visa.instrument(SCOPE_ADDR, values_format = visa.ascii)
    scope_preset(scope)
    return scope

def scope_get(scope, channel, points):
    vals = scope_get_raw(scope, channel, points)
    scaled = scope_get_scaledvals(scope, vals, channel)
    return scaled
    
def scope_get_raw(scope, channel, points):
    scope.write(":TRIGGER:SWEEP NORMAL")
    scope.write(":WAVEFORM:SOURCE CHANNEL " + str(channel))
    scope.write(":WAVEFORM:FORMAT ASCII")
    scope.write(":WAVEFORM:POINTS " + str(points))
    scope.write(":DIGITIZE CHANNEL" + str(channel))
    vals = scope.ask_for_values(":WAVEFORM:DATA?")[1:]
    return vals
    
def scope_settimebase(scope, base, delay):
    scope.write(":TIMEBASE:RANGE " + str(base) + "E-3") # set time base (in milliseconds)
    scope.write(":TIMEBASE:DELAY " + str(delay) + "E-3")
    scope.write(":TIMEBASE:REFERENCE CENTER")

def scope_get_scaledvals(scope, vals, channel):
    scale = float(scope.ask(":CHANNEL" + str(channel) + ':SCALE?'))
    offset = float(scope.ask(":CHANNEL" + str(channel) + ':OFFSET?'))
    att = float(scope.ask(":CHANNEL" + str(channel) + ':PROBE?'))
    span = float(scope.ask(":TIMEBASE:RANGE?"))
    delay = float(scope.ask(":TIMEBASE:DELAY?"))
    
    t = linspace(0,span,len(vals))
    return {'time':t, 'amp':vals}

def scope_setchannel(scope, channel, scale, att = 10, offset = 0, coupling = 'DC'):
    scope.write(":CHANNEL" + str(channel) + ':PROBE ' + str(att))
    scope.write(":CHANNEL" + str(channel) + ':SCALE ' + str(scale)) # set full range scale (in volts)
    scope.write(":CHANNEL" + str(channel) + ':OFFSET ' + str(offset)) # set offset (in volts)
    scope.write(":CHANNEL" + str(channel) + ':COUPLING ' + str(coupling))
    scope.write(":TIMEBASE:REFERENCE CENTER")

def scope_settrigger(scope, channel, level, slope = 'POSITIVE', mode = 'NORMAL', type = 'NORMAL'):
    scope.write(":TRIGGER:SWEEP " + mode)
    scope.write(":TRIGGER:LEVEL " + str(level))
    scope.write(":TRIGGER:SLOPE " + slope)
    scope.write(":ACQUIRE:TYPE " + type)

def scope_autoscale(scope):
    scope.write("AUTOSCALE")
    
def scope_preset(scope):
    scope.write("*RST")


# example usage: grabs and plots values from scope with correct time and amplitude scaling
if __name__ == "__main__":
    points = 200
    scope = scope_init()
    scope_autoscale(scope)
    vals =  scope_get(scope, 1, points)
    plot(vals['time'], vals['amp'])
    show()
    
