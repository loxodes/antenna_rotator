# jon klein, jtklein@alaska.edu
# mit license
# functions to automate current measurements

from pylab import *
from scope_control import *

CURRENT_MEASTIME = 100 # milliseconds
CURRENT_MEASDELAY = 0 # milliseconds
CURRENT_CHANNEL = 1
CURRENT_POINTS = 500
TRANSCONDUCTANCE_GAIN = 1.047#1.155


def measure_avgcurrent(scope, current_scale = TRANSCONDUCTANCE_GAIN, channel = CURRENT_CHANNEL, time = CURRENT_MEASTIME, delay = CURRENT_MEASDELAY):
    scope_settimebase(scope, time, delay)
    scope_setchannel(scope, channel, .1, att = 10, offset = .4)
    avg_voltage = average(scope_get_raw(scope, CURRENT_CHANNEL, CURRENT_POINTS))
    return (avg_voltage * TRANSCONDUCTANCE_GAIN)

if __name__ == '__main__':
    scope = scope_init()
 #   scope_setchannel(scope, 1, .1)
    current = 0
    for i in range(10):
        current = current + measure_avgcurrent(scope)
    print current / 10
    
