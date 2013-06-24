import shlex
import cmd
import serial
from retro_control import *
from rotator_control import *

BAUDRATE = 9600
TIMEOUT = .15
RATE = 4


class RetroConsole(cmd.Cmd):
    def do_serial(self, line):
        '''serial device port
        Open serial port for communicating with the array. 
        example: serial /dev/ttyUSB0
        '''
        self.ser = serial.Serial(line, BAUDRATE, timeout=TIMEOUT)

    def do_rserial(self, line):
        '''serial device port to rotator
        Open serial port for communicating with the antenna rotator. 
        example: rserial /dev/ttyUSB0
        '''
        self.rser = serial.Serial(line, BAUDRATE, timeout=TIMEOUT)

    def do_freq(self, line):
        '''freq value
        Sets the frequency of the ml2730 to value MHz
        example: freq 2450.25
        possible values are 2400 to 2480'''
        ml_freq(self.ser, line, rate)

    def do_spin(self, line):
        '''spin rate
        Sets the ml2730 into spin mode, with rate uS antenna switching speed
        example: switch 30
        valid switching rates are multiples of 10uS'''
        ml_spin(self.ser, line)

    def do_rxswitch(self, line):
        '''rxswitch channel
        Sets the ml2730 receive channel
        example: rxswitch 5
        valid channels are 1 to 6'''
        ml_rxswitch(self.ser, line)

    def do_rssi(self, line):
        '''rssi
        Reads the output power of transceiver in dBm
        example: rssi 1'''
        ml_rssi(self.ser)

    def do_aout(self, line):
        '''aout
        Reads the ml2730 frequency to analog output voltage pin
        example: aout'''
        ml_aout(self.ser)

    def do_roll(self, line):
        '''roll
        Sets the roll angle of the positioner in degrees (0 is upright)
        example: roll -10
        valid angles vary by servo, but are probably -180 to 180'''
        servo_setangle(self.rser, ROLL_CHANNEL, line)
        
    def do_flush(self, line):
        '''flush
        Flushes the input serial buffer
        example: flush'''
        self.ser.flushInput()
        
    def do_pan(self, line):
        '''pan
        Sets the pan angle of the positioner in degrees (0 is boresight)
        example: pan -10
        valid angles vary by servo, but are probably -180 to 180'''
        servo_setangle(self.rser, ROLL_CHANNEL, line)

    def do_tilt(self, line):
        '''tilt
        Sets the tilt angle of the positioner in degrees (0 is upright)
        example: tilt -10
        valid angles vary by servo, but are probably 0 to -90'''
        servo_setangle(self.rser, ROLL_CHANNEL, line)

    def do_mode(self, line):
        '''mode state
        Sets the mode (tx, rx, standby) an address 
        example: mode 5 tx  
        valid modes are tx, rx, and standby'''
        args = shlex.split(line)
        set_mode(self.ser, args[0], args[1])
    
    def do_stop(self, line):
        '''stop
        Stops all servo movements
        example: stop'''
        servo_stopall(eslf.rser)

    def do_reset(self, line):
        '''reset (ml, phase)
        Resets a target address 
        example: reset 5'''
        reset(self.ser, line)

    def do_phase(self, line):
        '''phase channel value
        Sets the phase offset of a address (in degrees)
        example: phase 1 150
        valid phase ranges are 0 to 200'''
        args = shlex.split(line)
        phase_set(self.ser, args[0], args[1])

    def do_dac_temp(self, line):
        '''dac_temp
        Checks the phase shifter driver amplifier for high temperature condition
        example: dac_temp'''
        checkdactemp(self.ser, line)

    def do_flushetx(self, line):
        '''flushetx
        Sends repeated ETX bytes to attempt to resync communication
        example: flushetx'''
        flush_etx(self.ser)

    def do_dac(self, line):
        '''dac channel value
        Sets the raw value of dac register
        example: dac b 2000
        valid phase ranges are 0 to 4096'''
        args = shlex.split(line)
        dac_set(self.ser, args[0], args[1])
    def do_ping(self, line):
        '''ping target
        Pings an address to check connectivity
        example: ping addr
        valid targets are 0 to 255'''
        args = shlex.split(line)
        board_ping(self.ser, args[0])
		
    def do_att(self, line):
        '''att channel value
        Sets the attenuation of a channel (in dB)
        example: att 4 20
        valid addresses are 0-255, valid attenuation is 0 to 30dB, in .25dB stepping'''
        args = shlex.split(line)
        att_set(self.ser, args[0], args[1])
        
    def do_steer(self, line):
        ''' steers the entire array to an az/el angle
        syntax is: steer az 
        example: steer 50
        '''
        args = shlex.split(line)
        array_steer(self.ser, args[0], 0)
        
    def do_EOF(self, line):
        return True
    
    def postloop(self):
        print

if __name__ == '__main__':
    print 'retrodirective array control application'
    print 'jon klein, kleinjt@ieee.org'
    print '----------------------------------------'
    print ''
    print 'you probably want to start by opening serial ports'
    print 'type help for a list of commands'
    print ''
    RetroConsole().cmdloop()

