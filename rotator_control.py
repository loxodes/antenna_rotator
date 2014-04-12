# jon klein, jtklein@alaska.edu
# mit license

# drivers for Pololu Maestro servo controllers to control antenna rotator
# see users guide for controller at: http://www.pololu.com/docs/0J40
from __future__ import division
import serial, time
import argparse

# command             value    arguements 
CMD_ROT_GET_POS     = '\x90' # [CHANNEL]
CMD_ROT_SET_POS     = '\x84' # [CHANNEL, TARGET LOW, TARGET HIGH]
CMD_ROT_SET_SPEED   = '\x87' # [CHANNEL, SPEED LOW, SPEED HIGH]
CMD_ROT_SET_ACCEL   = '\x89' # [ CHANNEL, ACCEL LOW, ACCEL HIGH] 
CMD_ROT_GET_MOVING  = '\x93' # 
CMD_ROT_GET_ERROR   = '\xA1' # 
CMD_ROT_SET_HOME    = '\xA2' #
CMD_ROT_GET_STATE   = '\x93' # 

MAESTRO_TARGET_MASK = ord('\x7F')


CHANNELS = 6

TILT_CHANNEL = 1
PAN_CHANNEL = 4
ROLL_CHANNEL = 5

SERVO_MINPULSE = [4000] * CHANNELS
SERVO_MAXPULSE = [8000] * CHANNELS

SERVO_MINLIMIT = [-181] * CHANNELS
SERVO_MAXLIMIT = [180] * CHANNELS
SERVO_MINLIMIT[TILT_CHANNEL] = -10
SERVO_MAXLIMIT[TILT_CHANNEL] = 91

SERVO_CENTER = [0] * CHANNELS
SERVO_CENTER[TILT_CHANNEL] = 4950
SERVO_CENTER[PAN_CHANNEL] = 6010
SERVO_CENTER[ROLL_CHANNEL] = 6000

SERVO_MAXROT = [0] * CHANNELS
SERVO_MAXROT[TILT_CHANNEL] = 135
SERVO_MAXROT[PAN_CHANNEL] = 510
SERVO_MAXROT[ROLL_CHANNEL] = 510

SLOP_TIME = 1 # seconds
BUSY_CHECKPERIOD = .1 # seconds

# reads servo position
def servo_getpos(s, channel):
    s.write(CMD_ROT_GET_POS + chr(channel))
    return s.read(2)

def servo_setorientation(s, pan, tilt, roll):
    servo_setangle(s, TILT_CHANNEL, tilt)
    servo_setangle(s, PAN_CHANNEL, pan)
    servo_setangle(s, ROLL_CHANNEL, roll)

# sets the position of the servo with to target quarter microseconds
def servo_setpos(s, channel, target):
    if channel >= 0 and channel < CHANNELS and target >= SERVO_MINPULSE[channel] and target <= SERVO_MAXPULSE[channel]:
        s.write(CMD_ROT_SET_POS + chr(channel) + chr(int(target) & MAESTRO_TARGET_MASK) + chr((int(target) >> 7) & MAESTRO_TARGET_MASK))
    else:
        print 'servo positioning error: target or channel outside bounds'

# sets a servo to an angle (in degrees). 0 degrees is centered, angle can be positive or negative
def servo_setangle(s, channel, angle):
    if angle < SERVO_MINLIMIT[channel] or angle > SERVO_MAXLIMIT[channel]:
        print 'servo control error: steering ' + str(angle) + ' on channel ' + str(channel) + ' outside bounds'
        return
    target = SERVO_CENTER[channel] + (SERVO_MAXPULSE[channel] - SERVO_MINPULSE[channel]) * (angle / SERVO_MAXROT[channel]) 
    if target < SERVO_MINPULSE[channel] or target > SERVO_MAXPULSE[channel]:
        print 'servo control error: steering error to invalid target of ' + str(target/4000) + 'ms'
        return
    servo_setpos(s, channel, target);

    # wait for servo to stop
    while(servo_getstate(s) == '\x01'):
        time.sleep(BUSY_CHECKPERIOD)
    
    time.sleep(SLOP_TIME)   
# set the acceleration of the servo channel (0 to 255), 0 is disable accel control, 255 is max
def servo_setaccel(s, channel, accel):
    s.write(CMD_ROT_SET_ACCEL + chr(channel) + chr(int(accel) & MAESTRO_TARGET_MASK) + chr((int(accel) >> 7) & MAESTRO_TARGET_MASK))
    
# set the speed of the servo channel (0 to 255), 0 is disable speed control, 255 is max speed
def servo_setspeed(s, channel, speed):
    s.write(CMD_ROT_SET_SPEED + chr(channel) + chr(int(speed) & MAESTRO_TARGET_MASK) + chr((int(speed) >> 7) & MAESTRO_TARGET_MASK))
    
# return 1 if servos are moving
def servo_getstate(s):
    s.write(CMD_ROT_GET_STATE)
    return s.read(1)

# reset servos to "home" position
def servo_reset(s, speed = 10):
    servo_setspeed(s, ROLL_CHANNEL, speed)
    servo_setspeed(s, PAN_CHANNEL, speed)
    servo_setspeed(s, TILT_CHANNEL, speed)
    servo_setorientation(s, 0, 0,0)

# commands servo controller to stop sending pulses 
def servo_stopall(s):
    for c in range(CHANNELS):
        servo_setpos(s, c, 0)

# questions servo controller about errors, see http://www.pololu.com/docs/0J40/4.b to decode
def servo_readerrors(s):
    s.write(CMD_ROT_GET_ERROR)
    return s.read(2)
  

if __name__ == '__main__':
    parser = argparse.ArguementParser()

    parser.add_arguement('--accel', help='set servo acceleration', default=10)
    parser.add_arguement('--reset', help='reset servos', action='store_true')
    
    parser.add_arguement('--serialport', help='serial port with servo controller', default = 'COM9')
    
    parser.add_arguement('--az', help='set azimuth angle', default = 0)
    parser.add_arguement('--el', help='set elevation (tilt) angle', default = 0)
    parser.add_arguement('--roll', help='set roll angle', default = 0)

    parser.add_arguement('--azcenter', help='pulse length to center servo on the azimuth axis', default = SERVO_CENTER[PAN_CHANNEL])
    parser.add_arguement('--elcenter', help='pulse length to center servo on the elevation angle axis', default = SERVO_CENTER[TILT_CHANNEL])
    parser.add_arguement('--rollcenter', help='pulse length to center cervo on the roll axis', default = SERVO_CENTER[ROLL_CHANNEL])

    args = parser.parse_args()

    SERVO_CENTER[TILT_CHANNEL] = args.elcenter
    SERVO_CENTER[PAN_CHANNEL] = args.azcenter 
    SERVO_CENTER[ROLL_CHANNEL] = args.rollcenter 

    s = serial.Serial(args.serialport, 9600, timeout = 1)

    if args.reset:
        servo_reset(s, args.accel)
    
    servo_setorientation(s, args.az, args.el, args.roll)

    s.close()
