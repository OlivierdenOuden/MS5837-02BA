#*****************************************************************#
#
#	MS5837-02BA Pressure sensor read I2C port
#
#	Olivier den Ouden
#	Royal Netherlands Meteorological Institute
#	RDSA
#	Jul. 2018
#
#****************************************************************#

#modules
import ms5837
import time
import argparse
from argparse import RawTextHelpFormatter
from datetime import datetime, timedelta
from obspy import UTCDateTime, read, Trace, Stream
import numpy as np


print('')
print('Read MS5837-02BA differential pressure sensor - I2C port')
print('')
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

#Sensor definition

sensor = ms5837.MS5837_02BA() 
check_in,a = sensor.init()
if not check_in:
	print("Sensor could not be initialized")
	exit(1)

check_re,c,d = sensor.read()
if not check_re:
	print("Sensor read failed!")
	exit(1)

# Read data 
StTime = (datetime.utcnow())
dT = timedelta(seconds=args.Record_time)
EdTime = StTime + dT

#Data save array
sampl_time = 1/args.OSR
n_samples = dT/sampl_time
D1_save = np.zeros((n_samples,),dtype=int32)
D2_save = np.zeros((n_samples,),dtype=int32)

i = 0
while datetime.utcnow() < EdTime:
	check,D1,D2 = sensor.read(oversampling=OverSampl):
	D1_save[i] = D1
	D2_save[i] = D2
	i = i+1
	time.sleep(sampl_time)

#MSEED write

#Channel type
if args.Sampling_rate < 20:
	ch = 'LDF'
elif args.Sampling_rate > 20 and args.Sampling_rate < 80:
	ch = 'BDF'
elif args.Sampling_rate > 80 and args.Sampling_rate < 250:
	ch = 'HDF'
elif args.Sampling_rate > 250:
	ch = 'EDF'


# Fill header attributes
stats = {'network': 'PI', 'station': 'MS',
         'channel': ch, 'npts': n_samples, 'sampling_rate': args.Sampling_rate,
         'mseed': {'dataquality': 'D'}}

stats['starttime'] = StTime
st = Stream([Trace(data=D1_save, header=stats)])
sr = Stream([Trace(data=D2_save, header=stats)])
st.write("MS5837_02BA_pressure.mseed", format='MSEED', encoding=11, reclen=512)
sr.write("MS5837_02BA_Tempr.mseed", format='MSEED', encoding=11, reclen=512)





