# jtklein@alaska.edu
# plot the estimated array gain with an increase in elements with a fixed power budget

from pylab import *
MAXCHANNELS = 32

channels = range(1, MAXCHANNELS+1)
array_power = 20 # watts
channel_overhead = .1 # watts
antenna_gain_ideal = 20*log10(log2(channels)) # 
pae = .3

array_gain = []
for i in range(MAXCHANNELS):
    array_gain.append(10*log10(1e3 * pae * (array_power -i * channel_overhead)) + antenna_gain_ideal[i])


plot(channels, array_gain)
grid(True)
xlabel('Channels in phased array')
ylabel('EIRP at boresight (dBm)')
xlim([1,32])
ylim([35,55])
title('Ideal EIRP of Phased Array at Boresight as size increases') 
show()
