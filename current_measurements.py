# jon klein, jtklein@alaska.edu
# mit license
# functions to automate current measurements

from pylab import *
from scope_control import *

CURRENT_MEASTIME = 100 # milliseconds
CURRENT_MEASDELAY = 0 # milliseconds
CURRENT_CHANNEL = 1
CURRENT_POINTS = 50
TRANSCONDUCTANCE_GAIN = 1.25

def measure_avgcurrent(scope, current_scale = TRANSCONDUCTANCE_GAIN, channel = CURRENT_CHANNEL, time = CURRENT_MEASTIME, delay = CURRENT_MEASDELAY):
    scope_autoscale(scope)
    scope_settimebase(scope, time, delay)
    avg_voltage = average(scope_get_raw(scope, CURRENT_CHANNEL, CURRENT_POINTS))
    return (avg_voltage * TRANSCONDUCTANCE_GAIN)

if __name__ == '__main__':
    scope = scope_init()
    scope_setchannel(scope, 1, .2)
    print measure_avgcurrent(scope)
    
    
