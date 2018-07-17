#*****************************************************************#
#
#	MS5837-02BA Pressure sensor Metadata I2C port
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
print('Metadata of MS5837-02BA differential pressure sensor')
print('')
print('')

sensor = ms5837.MS5837_02BA() 
check_in,a = sensor.init()
if not check_in:
	print("Sensor could not be initialized")
	exit(1)

check_re,c,d = sensor.read()
if not check_re:
	print("Sensor read failed!")
	exit(1)

#Collect metadata
check_in,C_variables = sensor.init()

#Save metadata
np.savetxt('Metadata_MS5837_02BA.txt',C_variables)