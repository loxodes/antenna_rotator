# jon klein, jtklein@alaska.edu
# mit license

# drivers for Pololu Maestro servo controllers to control antenna rotator
# see users guide for controller at: http://www.pololu.com/docs/0J40
from __future__ import division
import serial, time

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

SERVO_MINPULSE = 4000
SERVO_MAXPULSE = 8000

SERVO_CENTER = [0] * CHANNELS
SERVO_CENTER[TILT_CHANNEL] = 6000 #TBD
SERVO_CENTER[PAN_CHANNEL] = 6000 #TBD
SERVO_CENTER[ROLL_CHANNEL] = 6000 #TBD

SERVO_MAXROT = [0] * CHANNELS
SERVO_MAXROT[TILT_CHANNEL] = 135
SERVO_MAXROT[PAN_CHANNEL] = 520
SERVO_MAXROT[ROLL_CHANNEL] = 510

SLOP_TIME = 2 # seconds
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
    if channel >= 0 and channel < CHANNELS and target >= SERVO_MINPULSE and target <= SERVO_MAXPULSE:
        s.write(CMD_ROT_SET_POS + chr(channel) + chr(int(target) & MAESTRO_TARGET_MASK) + chr((int(target) >> 7) & MAESTRO_TARGET_MASK))
    else:
        print 'servo positioning error: target or channel outside bounds'

# sets a servo to an angle (in degrees). 0 degrees is centered, angle can be positive or negative
def servo_setangle(s, channel, angle):
    target = SERVO_CENTER[channel] + (SERVO_MAXPULSE - SERVO_MINPULSE) * (angle / SERVO_MAXROT[channel]) 
    if target < SERVO_MINPULSE or target > SERVO_MAXPULSE:
        print 'servo control error: steering error to invalid target of ' + str(target/4000) + 'ms'
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
def servo_reset(s):
    servo_setspeed(s, ROLL_CHANNEL, 10)
    servo_setspeed(s, PAN_CHANNEL, 10)
    servo_setspeed(s, TILT_CHANNEL, 10)
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
    s = serial.Serial('COM9', 9600, timeout = 1)
    servo_setspeed(s, ROLL_CHANNEL, 2)
    servo_setaccel(s, ROLL_CHANNEL, 0)
