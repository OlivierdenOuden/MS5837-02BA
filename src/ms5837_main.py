#******************************************************************************#
#														
#		MS5837 - TE Connectivity Pressure sensor		
#														
#		Main script with defenitions, can be called		
#		by a read-out script.							
#														
#		Olivier den Ouden								
#		Royal Netherlands Meterological Institute		
#		RD Seismology and Acoustics						
#		https://www.seabirdsound.org 					
#														
#*******************************************************************************#

# Modules
import smbus
import time 
import numpy as np

bus = smbus.SMBus(1)

# Oversampling options
OSR_256  = 0
OSR_512  = 1
OSR_1024 = 2
OSR_2048 = 3
OSR_4096 = 4
OSR_8192 = 5
    
# MS5837 hex adress
MS5837_ADDR             = 0x76
MS5837_RESET            = 0x1E
MS5837_ADC_READ         = 0x00
MS5837_PROM_READ        = 0xA0
MS5837_CONVERT_D1       = 0x40
MS5837_CONVERT_D2       = 0x50

        
def calibration():
    # Reset the device    
	bus.write_byte(MS5837_ADDR,MS5837_RESET)
	time.sleep(2)
    
    # Read calibration values    
	C = np.zeros((7))
	for i in range(0,7):
		c = bus.read_word_data(MS5837_ADDR, MS5837_PROM_READ+2*i)
		c =  ((c & 0xFF) << 8) | (c >> 8) 
		C[i] = c

	return True, C
	        
def read(oversampling=OSR_8192):
        
	if oversampling < OSR_256 or oversampling > OSR_8192:
		print "Invalid oversampling!"
		return False
        
	# D1 read/write (pressure)
	bus.write_byte(MS5837_ADDR, MS5837_CONVERT_D1 + 2*oversampling)
	time.sleep(2.5e-6 * 2**(8+oversampling))
        
	d = bus.read_i2c_block_data(MS5837_ADDR,MS5837_ADC_READ,3)
	D1 = d[0] << 16 | d[1] << 8 | d[2]
        
	# D2 read/write (temperature)
	bus.write_byte(MS5837_ADDR,MS5837_CONVERT_D2 + 2*oversampling)
	time.sleep(2.5e-6 * 2**(8+oversampling))
 
	d = bus.read_i2c_block_data(MS5837_ADDR,MS5837_ADC_READ,3)
	D2 = d[0] << 16 | d[1] << 8 | d[2]

        
	return True,D1,D2

# Convert data counts into temperature/pressure    
def calculate(C,D1,D2):

	# First order convertion
	Ti = 0
	OFFi = 0
	SENSi= 0

	dT = D2-(C[5]*256)
	Temperature = (2000+np.int32(dT)*C[6]/8388608)
	
	OFF = np.int64(C[2]*131072 + (C[4]*np.int32(dT))/64)
	SENS= np.int64(C[1]*65536 + (C[3]*np.int32(dT))/128)
	Pressure = D1*np.int64(SENS)/2097152-np.int64(OFF)/32768

    # Second order compensation
	if (Temperature/100) < 20: 
		Ti = (11*np.int32(dT)*np.int32(dT))/(34359738368)
		OFFi = (31*(Temperature-2000)*(Temperature-2000))/8
		SENSi = (63*(Temperature-2000)*(Temperature-2000))/32
	
	OFF2 = OFF-OFFi
	SENS2 = SENS-SENSi

	Temperature = (Temperature-Ti)/100.0
	Pressure = (((D1*np.int64(SENS2))/2097152-np.int64(OFF2))/32768)/100.0

	return Temperature,Pressure

# Check CRC4
def crc4(n_prom):
	n_rem = 0
        
	n_prom[0] = ((n_prom[0]) & 0x0FFF)
	n_prom.append(0)
    
	for i in range(16):
		if i%2 == 1:
			n_rem ^= ((n_prom[i>>1]) & 0x00FF)
		else:
			n_rem ^= (n_prom[i>>1] >> 8)
                
		for n_bit in range(8,0,-1):
			if n_rem & 0x8000:
				n_rem = (n_rem << 1) ^ 0x3000
			else:
				n_rem = (n_rem << 1)

	n_rem = ((n_rem >> 12) & 0x000F)
        
	n_prom = n_prom
	n_rem = n_rem
    
	return n_rem ^ 0x00
