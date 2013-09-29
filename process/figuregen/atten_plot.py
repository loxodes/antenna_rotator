from __future__ import division
from pylab import *
def dbtolin(d):
  return 10 ** (d/10)

rcParams['legend.loc'] = 'best'

phase_shifter_atten = dbtolin(4.5) # dB
attenuator_atten = dbtolin(4) # worst case
tr_attenuation = dbtolin(.64)
amp_gain = dbtolin(35)
labels = ['T/R Switch Loss', 'Phase Shifter Loss', 'Attenuator Loss']
pout = range(0, 26)
poutlin = [dbtolin(p) for p in pout]

trloss = [pl * (1 - 1/tr_attenuation) for pl in poutlin]
psloss = [(pl * tr_attenuation / amp_gain) * (1 - 1/phase_shifter_atten)  for pl in poutlin]
atloss = [(1 - 1/attenuator_atten) * (pl * tr_attenuation * phase_shifter_atten / amp_gain) for pl in poutlin]

plot(pout, trloss)
plot(pout, psloss)
plot(pout, atloss)
legend(labels)
grid(True)
xlabel('Phased Array Module Output Power (dBm)')
ylabel('Power Loss from Attenuation (mW)')
title('Calculated power overhead from phase shifter, attenuator, and T/R switch in a phase array module as a function of output power.')
savefig('txpath_comploss.png', bbox_inches='tight')
show()

