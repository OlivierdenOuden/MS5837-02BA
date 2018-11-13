#*****************************************************************#
#
#	MS5837-02BA Pressure sensor read I2C port
#
#	Olivier den Ouden
#	Royal Netherlands Meteorological Institute
#	RDSA
#	Oct. 2018
#
#****************************************************************#

#modules
import I2Cread_ms5837 as read
import time
import argparse
from argparse import RawTextHelpFormatter
from datetime import datetime, timedelta
from obspy import UTCDateTime, read, Trace, Stream
import numpy as np

print('')
print('Read MS5837-02BA differential pressure sensor - I2C port')
print('')
print('Olivier den Ouden')
print('Royal Netherlands Meteorological Institute, KNMI')
print('Oct. 2018')
print('')


parser = argparse.ArgumentParser(prog='Import pressure data of the MS5837-02BA.',
    description=('Main script to import differential pressure data of the MS5837-02BA\n'
        'to a Raspberry Pi. Data formt is MSEED. \n'
    ), formatter_class=RawTextHelpFormatter
)


parser.add_argument(
    '--OSR',action='store', default=8192, type=float,
    help=('Oversampling rate (default: %(default)s Hz)\n'),
    metavar='8192')

parser.add_argument(
    '--Record_time',action='store', default=3600, type=float,
    help=('Time of recording (default: %(default)s sec)\n'),
    metavar='3600')

parser.add_argument(
    '-v',action='store', default=0, type=float,
    help=('Verbose, 0=off 1=on (default: %(default)s)\n'),
    metavar='0')

args = parser.parse_args()


#Oversmapling value
if args.OSR == 8192:
	OverSampl = 5
elif args.OSR == 4096:
	OverSampl = 4
elif args.OSR == 2048:
	OverSampl = 3
elif args.OSR == 1024:
	OverSampl = 2
elif args.OSR == 512:
	OverSampl = 1
elif args.OSR == 256:
	OverSampl = 0

#Time
StTime = (datetime.utcnow())
dT = timedelta(seconds=args.Record_time)
EdTime = StTime + dT

#Data save array
sampl_time = 1/args.OSR
n_samples = np.int(dT.seconds/sampl_time)
C_values = np.zeros((7))
D1_save = np.zeros((n_samples,),dtype=np.int32)
D2_save = np.zeros((n_samples,),dtype=np.int32)

i = 0
while datetime.utcnow() < EdTime:
	
	#Reset and Calibration values
	if i ==0:
		check,C_values = read.MS5837_start()
		if check==True:
			print('')
			print('Sensor reset, Calibration values saved')
			print('Ready to record...')
			print('')
		else:
			print('')
			print('ERROR')
			print('Sensor reset, Calibration values')
			print('')

	#Read data
	check,D1,D2 = read.read(oversampling=5)
	if args.v == 1:
		if check == True:
			print(datetime.utcnow(),'Sample ',i,'NO ERROR')
		else:
			print(datetime.utcnow(),'Sample ',i,'ERROR in recording')
	D1_save[i] = D1
	D2_save[i] = D2
	i = i+1

#MSEED write

#Channel type
if args.OSR < 20:
	ch = 'LDF'
elif args.OSR > 20 and args.OSR < 80:
	ch = 'BDF'
elif args.OSR > 80 and args.OSR < 250:
	ch = 'HDF'
elif args.OSR > 250:
	ch = 'EDF'


# Fill header attributes
stats = {'network': 'PI', 'station': 'MS',
         'channel': ch, 'npts': n_samples, 'sampling_rate': args.OSR,
         'mseed': {'dataquality': 'D'}}

stats['starttime'] = StTime
st = Stream([Trace(data=D1_save, header=stats)])
sr = Stream([Trace(data=D2_save, header=stats)])
st.write("MS5837_02BA_pressure.mseed", format='MSEED', encoding=11, reclen=512)
sr.write("MS5837_02BA_Tempr.mseed", format='MSEED', encoding=11, reclen=512)





