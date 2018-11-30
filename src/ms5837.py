#****************************************************************************#
#														
#		MS5837 - TE Connectivity Pressure sensor		
#														
#		Read-out script.								
#														
#		Olivier den Ouden								
#		Royal Netherlands Meterological Institute		
#		RD Seismology and Acoustics						
#		https://www.seabirdsound.org 					
#														
#****************************************************************************#


# Modules
import ms5837_main
import smbus
import time 
import numpy as np
from datetime import datetime
import argparse
from argparse import RawTextHelpFormatter

print('')
print('MS5837 TE Connectivity Pressure sensor Read-out')
print('')
print('Olivier den Ouden')
print('Royal Netherlands Meteorological Institute, KNMI')
print('Dec. 2018')
print('')

# Parser arguments
parser = argparse.ArgumentParser(prog='MS5837 TE Connectivity Pressure sensor Read-out',
    description=('Read-out of the MS5837 TE Connectivity Pressure sensor\n'
    ), formatter_class=RawTextHelpFormatter
)

parser.add_argument(
    '-t', action='store', default=100, type=float,
    help='Time of recording, [sec].\n', metavar='-t')

parser.add_argument(
    '-fs', action='store', default=1, type=float,
    help='Sample rate, [Hz].\n', metavar='-fs')

parser.add_argument(
    '-OverSamp', action='store', default=5, type=float,
    help='Oversampling rate, [Hz].\n', metavar='-OverSamp')

args = parser.parse_args()

# Check if MS can comunicate with SL
Check,C = ms5837_main.calibration()
if Check == True:
	print "Sensor MS5837 initialized"
else:
	print "Sensor MS5837 could not be initialized"
	exit(1)

# Time knowledge
st = datetime.utcnow()
fs = args.fs
record_t = args.t
n_samples = record_t*fs
oversampling = args.OverSamp

# Save data
Time_array = np.linspace(0,record_t,n_samples)
Temp = np.zeros((n_samples,2))
Pres = np.zeros((n_samples,2))
Temp[:,0] = Time_array[:]
Pres[:,0] = Time_array[:]

# Loop 
i = 0
while i < n_samples:
	check_,p_data,t_data = ms5837_main.read(oversampling)
	Temp[i,1] = t_data
	Pres[i,1] = p_data
	i = i+1

	# Print converted data
	read_Temp,read_Pres = ms5837_main.calculate(C,p_data,t_data)
	print("Temp: %0.2f C  P: %0.2f hPa ") % (read_Temp,read_Pres)

	# Sampling rate
	time.sleep(1/fs)






