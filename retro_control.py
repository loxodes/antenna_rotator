import serial
import binascii
import struct
import time
import pdb
from pylab import *

ACK = '\x06'
NAK = '\x15'
STX = '\x02'
ETX = '\x03'
ENQ = '\x05'
RS = '\x1E'
SOH = '\x01'

CMD_ML_FREQ_SET = '\x31'
CMD_ML_SPIN_SET = '\x33'
CMD_ML_SWITCH_SET = '\x35'
CMD_ML_RSSI_READ = '\x36'
CMD_ML_AOUT_READ = '\x38'
CMD_ML_MODE_READ = '\x3C'
CMD_ML_MODE_SET = '\x3D'
CMD_ML_DISP = '\x3E'

CMD_PA_DAC_READ = '\xD0'
CMD_PA_DAC_SET = '\xD1'
CMD_PA_DET_READ = '\xD2'
CMD_PA_DAC_THERM_READ = '\xD4'
CMD_PA_ATT_READ = '\xD6'
CMD_PA_ATT_SET = '\xD7'
CMD_PA_ATT_SET_RAW = '\xDB'
CMD_PA_PHASE_READ = '\xD8'
CMD_PA_PHASE_SET = '\xD9'
CMD_PA_PHASE_SET_RAW = '\xDA'
CMD_PA_MODE_READ =  '\xDC'
CMD_PA_MODE_SET = '\xDD'

CMD_DISP = '\xDE'
CMD_RESET = '\xDF'
CMD_PING = '\xE0'

STANDBY_MODE = 0
RECEIVE_MODE = 1
TRANSMIT_MODE = 2

RS485_MAX_TRIES = 4
COMMAND_DELAY = .1 # seconds
HOST_ADDR = '\x07'

ARRAY_CONFIG = ['e', 'f']
ARRAY_SPACING = .45 # wavelengths

# STX CMD LEN PAYLOAD ETX
def cmd_send(s, taddr, cmd, payload = ''):
    i = 0

    while(True):
        i = i + 1;
        s.flushInput()

        command = ETX + ETX + ENQ + short_pack(ord(taddr)) + RS + short_pack(ord(HOST_ADDR)) + STX + SOH + cmd + chr(len(payload)) + payload + ETX
        s.write(command)
       
        if not 'ACM' in s.port: # don't readback if using ezdebug (direct serial)
            readback = s.read(len(command))
            if readback != command:
                print 'warning: command readback failed. is the bus busy?'
                print 'readback: ' + str([hex(ord(c)) for c in readback]) + ' expected ' + str([hex(ord(c)) for c in command])
        
        # TODO: FLUSH SERIAL BUFFER AND RE SEND COMMAND IF REPONSE FAILS
        r = response_read(s)
        
        if(r['k'] == ACK):
            break
            
        if i > RS485_MAX_TRIES:
            print 'warning: retry limit RS485_MAX_TRIES exceeded, giving up on command..'
            break
            
        print 'warning: command send #' + str(i) + ' failed, attempting again'
        time.sleep(.1)
    return r 

def response_read(s):
    # TODO: ADD SYNC
    response = ''
    if s.read(1) != ENQ:
        print 'warning: no ENQ, out of sync'
    
    taddr = s.read(2)
    
#    if taddr[0] + taddr[1] != HOST_ADDR:
#        print 'warning: target address mismatch on response'
    
    if s.read(1) != RS:
        print 'warning: no RS, out of sync'
         
    saddr = s.read(2)
    
    if s.read(1) != STX:
        print 'warning: no STX, out of sync'
    
    k = s.read(1)

    if k == ACK:
        cmd = s.read(1)
        length = s.read(1)
        payload = s.read(ord(length))
        end = s.read(1)
        response = ACK
   
    else: 
        print 'warning: NAK'
        cmd = s.read(1)
        payload = ''
        end = s.read(1)
        response = NAK

    if end != ETX:
        print 'warning: end of serial response is not ETX!'
    
    return {'cmd':cmd, 'payload':payload, 'k':k}
    
# flushes etx, maybe resyncs communication 
def flush_etx(s):
    s.write(ETX * 20)

def short_unpack(word):
    if(len(word) != 2):
        print 'error: word ' + word + ' not of correct length, returning 0'
        return 0
    return struct.unpack('H', word)[0]

def short_pack(value):
    return struct.pack('H', value)

def att_set(s, addr, value):
    r = cmd_send(s, addr, CMD_PA_ATT_SET, short_pack(int(value)))
    time.sleep(COMMAND_DELAY)
    return r['k']
    
def att_set_raw(s, addr, value):
    r = cmd_send(s, addr, CMD_PA_ATT_SET_RAW, short_pack(int(value)))
    time.sleep(COMMAND_DELAY)
    return r['k']
    
def dac_set(s, addr, value):
    r = cmd_send(s, addr, CMD_PA_DAC_SET, short_pack(int(value)))
    return r['k']
    
def checkdactemp(s):
    r = cmd_send(s, addr, CMD_PA_DAC_THERM_READ)
    return short_unpack(r['payload'])

def phase_set(s, addr, value):
    r = cmd_send(s, addr, CMD_PA_PHASE_SET, short_pack(int(value)))
    time.sleep(COMMAND_DELAY)
    return r['k']

def phase_set_raw(s, addr, value):
    r = cmd_send(s, addr, CMD_PA_PHASE_SET_RAW, short_pack(int(value)))
    time.sleep(COMMAND_DELAY)
    return r['k']

def att_get(s, addr):
    r = cmd_send(s, addr, CMD_PA_ATT_GET)
    return short_unpack(r['payload'])

def phase_get(s, addr):
    r = cmd_send(s, addr, CMD_PA_PHASE_GET)
    return short_unpack(r['payload'])


def reset(s, addr, target = ''):
    r = cmd_send(s, addr, CMD_RESET)
    return r['k']

def board_ping(s, addr):
    r = cmd_send(s, addr, CMD_PING)
    return r['k']

def ml_read_aout(s):
    r = cmd_send(s, CMD_ML_AOUT_READ)
    return short_unpack(r['payload'])

def ml_rssi(s):
    r = cmd_send(s, CMD_ML_RSSI_READ)
    return short_unpack(r['payload'])

def ml_rxswitch(s, switch):
    r = cmd_send(s, CMD_ML_SWITCH_SET, short_pack(switch)) 
    return r['k']

def ml_spin(s, rate):
    r = cmd_send(s, CMD_ML_SPIN_SET, short_pack(rate) / 10)
    return r['k'] 

def ml_freq(s, freq, rate):
    divbaseoffs = 8

    if rate == 0 or rate == 1:
        h = divbaseoffs + 107
        fref = 13.824e6
        istep = 20.736
        base = 1.5 * fref * H 
    
    if rate == 2 or rate == 3 or rate == 4:
        h = divbaseoffs + 122
        fref = 12.288e6
        istep = 18.432
    
    fstep = 1.5 * fref / (pow(2,20))
    base = 1.5 * fref * H
    margin = freq - base
    ipart = int(margin / istep)
    fpart = int((margin - ipart * istep)/fstep)
    
    payload = chr(ipart) + SOH + chr(fpart >> 16) + short_pack(fpart & 0xFFFF)
    r = cmd_send(s, CMD_ML_FREQ_SET, payload) 
    return r['k']

def set_mode(s, addr, mode):
    if mode == 'transmit' or mode == 'tx':
        m = TRANSMIT_MODE
    elif mode == 'receive' or mode == 'rx':
        m = RECEIVE_MODE
    else:
        m = STANDBY_MODE

    r = cmd_send(s, addr, CMD_PA_MODE_SET, short_pack(m))
    time.sleep(COMMAND_DELAY)
    return r['k']

# steers the array to az, el (degrees) (el is ignored)
def array_steer(s, az, el = 0):
    dphase = 360 * sin(deg2rad(int(az))) * ARRAY_SPACING;
    
    time.sleep(.15)

    if(dphase > 0):
        for i in range(len(ARRAY_CONFIG)):
            phase_set(s, ARRAY_CONFIG[i], int(i * dphase))
            time.sleep(.10)
    else:
        for i in range(len(ARRAY_CONFIG)):
            phase_set(s, ARRAY_CONFIG[i], int((len(ARRAY_CONFIG) - i) * abs(dphase)))
            time.sleep(.10)
    

    
if __name__ == "__main__":
    s = serial.Serial('COM8', 9600, timeout=.1)
    
    for i in range(10000):
        print 'attempt : ' + str(i)
        cmd_send(s, 'e', CMD_PING, payload = '')
