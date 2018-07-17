#*****************************************************************#
#
#	MS5837-02BA Pressure sensor convert MSEED
#
#	Olivier den Ouden
#	Royal Netherlands Meteorological Institute
#	RDSA
#	Jul. 2018
#
#****************************************************************#

#Modules
import ms5837
import time
import argparse
from argparse import RawTextHelpFormatter
from datetime import datetime, timedelta
from obspy import UTCDateTime, read, Trace, Stream
import numpy as np


print('')
print('Convertion of raw data, MS5837-02BA differential pressure sensor')
print('')
print('')

Metadata = np.loadtxt('Metadata_MS5837_02BA.txt')
C_1 = Metadata[1]
C_2 = Metadata[2]
C_3 = Metadata[3]
C_4 = Metadata[4]
C_5 = Metadata[5]
C_6 = Metadata[6]

# Temperature
Tmp = read('MS5837_02BA_Tempr.mseed.mseed')
Prs = read('MS5837_02BA_pressure.mseed')
stats = Prs[0].stats

n_samples = len(Tmp)

for i in range(0,n_samples):
	#Calc Temperature
	dT = Tmp[i] - C_2*256
	Tmp[i] = 2000 + dT*C_6/8388608

	#Calc temp compensated Pressure
	Off = C_2*131072 + (C_4*dT)/64
	Sens= C_1*65536 + (C_3*dT)/128
	Prs[i] = (Prs[i]*Sens/2097152 - Off)/32768

st = Stream([Trace(data=Prs, header=stats)])
st.write("Conv_MS5837_02BA_pressure.mseed", format='MSEED', encoding=11, reclen=512)




