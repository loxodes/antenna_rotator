antenna_rotator
===============

Python scripts to automate antenna measurements in the University of Alaska, Fairbanks microwave lab and anechoic chamber.
Written by Jon Klein and Russell Carroll

Usage Instruction:

1. Attach antenna to rotator plate, connect SMA cable to antenna
2. Turn on VNA and apply calibration (anechoic_klein_may3_13_1g_to_3g_801pts_0dbm would work)
3. Plug "TO ANECHOIC CHAMBER" USB cable in to workstation computer
4. Set a power supply to 6V, plug "SERVO POWER 6V" cable in to power supply
5. Run patch_capture.py
6. Enter the name of a directory to save files in when prompted

The patch_capture program will create several files:
* antenna_s11.s1p - a s1p file of the antenna at boresight
* radpattern.png - a plot comparing the radiation pattern of the antenna with pan at 0 and 90 degrees rotation
* rot0.csv - a CSV file containing the gain of the antenna with pan at 0 degrees rotation 
* rot90.csv - a CSV file containing the gain of the antenna with pan at 90 degrees rotation
* antenna_measurements_xx_xx_xx_xx_xx.hdf5 - an hdf5 archive containing all the raw s-parameter measurements

When you are done, unplug in USB cable and servo power supply cables in any order. Take the files from the directory you specified.
