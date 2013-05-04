antenna_rotator
===============

Python scripts to automate antenna measurements in the University of Alaska, Fairbanks microwave lab and anechoic chamber.


Usage Instruction:
0. Attach antenna to rotator plate, connect SMA cable to antenna.
1. Turn on VNA, apply calibration and set power levels.
2. Plug in "TO ANECHOIC CHAMBER" USB cable to workstation computer.
3. Set a power supply to 6V, plug "SERVO POWER 6V" cable in to power supply.
4. Run patch_capture.py


The patch_capture program will create several files:
* antenna_s11.s1p - a s1p file of the antenna at boresight
* radpattern.png - a plot comparing the radiation pattern of the antenna with pan at 0 and 90 degrees rotation
* rot0.csv - a CSV file containing the gain of the antenna with pan at 0 degrees rotation 
* rot90.csv - a CSV file containing the gain of the antenna with pan at 90 degrees rotation
* antenna_measurements_xx_xx_xx_xx_xx.hdf5 - an hdf5 archive containing all the raw s-parameter measurements