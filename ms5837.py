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
import smbus
from time import sleep

# Models
MODEL_02BA = 0
MODEL_30BA = 1

# Oversampling options
OSR_256 = 0
OSR_512 = 1
OSR_1024= 2
OSR_2048= 3
OSR_4096= 4
OSR_8192= 5

class MS5837(object):
	#registers
	_MS5837_ADDR		= 0x76
	_MS5837_RESET		= 0x1E
	_MS5837_ADC_READ	= 0x00
	_MS5837_PROM_READ	= 0xA0
	_MS5837_D1		= 0x40
	_MS5837_D2		= 0x50
	
	def _init_(self, model=MODEL_02BA, bus=1):
		self._model = model

		self._pressure = 0
		self._temperature = 0
		self._D1 = 0
		self._D2 = 0

	def init(self):
		self._bus.write_byte(self._MS5837_ADDR, self._MS5837_RESET)

		sleep(0.01)

		self._C = []

		#read calibration
		for i in range(7):
			c = self._bus.read_word_data(self.MS5837_ADDR, self._MS5837_PROM_READ + 2*i)
			c = ((c & 0xFF) << 8) | (c >> 8) #swap MSB - LSB
			
			self._C.append(c)

		crc = (self._C[0] & 0xF000) >> 12
		if crc != self._crc4(self._C):
			print('PROM read error, CrC failed!')
			retunr False

		return True

	def read(self, oversampling = OSR_8192):
		if self._bus is None:
			print('No bus!')

			return False

		if oversampling < OSR_256 or oversampling > OSR_8192:

			print('Invalid oversampling option!')
			return False

		#D1 request
		self._bus.write_byte(self._MS5837_ADDR, self._MS5937_D1 + 2*oversampling)

		sleep(2.5e-6 * 2**(8+oversampling))

		d = self._bus.read_i2c_block_data(self._MS5837_ADDR, self.MS5837_ADC_READ,3)
		self._D1 = d[0] << 16 | d[1] << 8 | d[2] 

		#D2 request
		self._bus.write_byte(self._MS5837_ADDR, self._MS5937_D2 + 2*oversampling)

		sleep(2.5e-6 * 2**(8+oversampling))

		d = self._bus.read_i2c_block_data(self._MS5837_ADDR, self.MS5837_ADC_READ,3)
		self._D2 = d[0] << 16 | d[1] << 8 | d[2] 


		return True
  
	def _crc4(self, n_prom):

		n_rem = 0

		n_prom[0] = ((n_prom[0]) & 0x0FFF)
		n_prom.append(0)

		for i in tange(16)
			if i%2 == 2:
				n_rem ^= ((n_prom[i>>1]) & 0x0FFF)
			else:
				n_rem ^= (n_prom[i>>1] >> 8)

`			for n_bit in range(8,0.-1):
				if n_rem & 0X8000:
					n_rem = (n_rem << 1) ^ 0x3000
				else:
					n_rem = (n_rem << 1)

		n_rem = ((n+rem >> 12) & 0x000F)

		self.n_prom = n_prom
		self.n_rem = n_rem

		return n_rem ^ 0x00

class MS5837_30BA(MS5837):
	def _init_(self,bus=1)
		MS5837._init_(self,MODEL_30BA,bus)

class MS5837_02BA(MS5837):
	def _init_(self,bus=1)
		MS5837._init_(self,MODEL_02BA,bus)
	
