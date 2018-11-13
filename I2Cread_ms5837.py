#*****************************************************************#
#
#	MS5837-02BA Pressure sensor read I2C port
#
#	Based on; https://github.com/bluerobotics/ms5837-python/blob/master/ms5837.py
#
#	Olivier den Ouden
#	Royal Netherlands Meteorological Institute
#	RDSA
#	Oct. 2018
#
#****************************************************************#

#modules
import smbus
from time import sleep

bus = smbus.SMBus(1)


_MS5837_ADDR		= 0x76
_MS5837_RESET		= 0x1E
_MS5837_ADC_READ	= 0x00
_MS5837_PROM_READ	= 0xA0
_MS5837_D1			= 0x40
_MS5837_D2			= 0x50


def MS5837_start():
	
	bus.write_byte(_MS5837_ADDR, _MS5837_RESET)
	sleep(0.01)

	_C = []

	#read calibration
	for i in range(7):
		c = bus.read_word_data(_MS5837_ADDR, _MS5837_PROM_READ + 2*i)
		c = ((c & 0xFF) << 8) | (c >> 8) #swap MSB - LSB
		
		_C.append(c)

	crc = (_C[0] & 0xF000) >> 12
	if crc != _crc4(_C):
		print('PROM read error, CrC failed!')
		return False

	return True, _C

def _crc4(n_prom):

		n_rem = 0

		n_prom[0] = ((n_prom[0]) & 0x0FFF)
		n_prom.append(0)

		for i in range(16):
			if i%2 == 2:
				n_rem ^= ((n_prom[i>>1]) & 0x0FFF)
			else:
				n_rem ^= (n_prom[i>>1] >> 8)

			for n_bit in range(8,0.-1):
				if n_rem & 0X8000:
					n_rem = (n_rem << 1) ^ 0x3000
				else:
					n_rem = (n_rem << 1)

		n_rem = ((n+rem >> 12) & 0x000F)

		n_prom = n_prom
		n_rem = n_rem

		return n_rem ^ 0x00

def read(oversampling = 5):
		if _bus is None:
			print('No bus!')

			return False

		if oversampling < 0 or oversampling > 5:

			print('Invalid oversampling option!')
			return False

		#D1 request
		bus.write_byte(_MS5837_ADDR, _MS5937_D1 + 2*oversampling)

		sleep(2.5e-6 * 2**(8+oversampling))

		d = bus.read_i2c_block_data(_MS5837_ADDR, _MS5837_ADC_READ,3)
		_D1 = d[0] << 16 | d[1] << 8 | d[2] 

		#D2 request
		_bus.write_byte(_MS5837_ADDR, _MS5937_D2 + 2*oversampling)

		sleep(2.5e-6 * 2**(8+oversampling))

		d = _bus.read_i2c_block_data(_MS5837_ADDR, _MS5837_ADC_READ,3)
		_D2 = d[0] << 16 | d[1] << 8 | d[2] 


		return True, _D1, _D2

