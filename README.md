# MS5837_02BA sensor 

How to read-out MS5837_02BA digital differetial pressure sensor by use of the I2C port on a Raspberry PI model 3B+. More info on the [MS5837 sensor](http://www.te.com/commerce/DocumentDelivery/DDEController?Action=srchrtrv&DocNm=MS5837-02BA01&DocType=Data+Sheet&DocLang=English&DocFormat=pdf&PartCntxt=CAT-BLPS0059) and the [I2C port](https://learn.sparkfun.com/tutorials/raspberry-pi-spi-and-i2c-tutorial).

## Raspberry PI - I2C port 

First the hardware needs to be enabled before the software, attached python scripts, can be used. This is done by following the steps of the link above.
The I2C port is not enabled by default, this needs to be done;
1. Run, in terminal, ```sudo raspi-config```.
2. Select point 9, ```Advanced options```.
3. Select A7, ```I2C```, and select ```yes```.
4. Exit this window and reboot the PI.

After reboot, check if the I2C port is enabled by using;

```
ls /dev/*i2c*
```

if I2C port is open the PI will respond with;

```
/dev/i2c-1
```

where ```1``` indicates which I2C bus is used.

Now the I2C port is enabled but to have interaction between the PI and the sensor some utilities are needed. Use the following command line in a terminal;

```
sudo apt-get install -y i2c-tools
```

The ```i2cdetect``` command probes all the addresses on a I2C port bus, and report whether any devices are present. Outcome of this command will look like;

```
pi@raspberrypi:~/$ i2cdetect -y 1
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:          -- -- -- -- -- -- -- -- -- -- -- -- --
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
60: 60 -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
70: -- -- -- -- -- -- -- --
```

Here the I2C adress of the sensor is 0x60. More information, or source, can be found [here](https://learn.sparkfun.com/tutorials/raspberry-pi-spi-and-i2c-tutorial).

## I2C - Python 

To read out the sensors with python, some python modules are needed. Run the command lines below;

```
sudo apt-get update
sudo apt-get install python-smbus
sudo apt-get install python-obspy
```

## Python scripts

The main file to read raw sensor data of the MS5837-02BA is the ```read_ms5837.py``` script. This script calls ```ms5837.py```, wherein all needed defenitions are listed. When calling the main script some arguments are needed, [source](https://github.com/bluerobotics/ms5837-python/blob/master/ms5837.py);

```
OSR           - Oversampling rate
Record time   - Recording time
```
To create a metadata file to convert the raw data, use ```inv_ms5837.py```. Converting raw data, counts, to temperature and pressure is done by ```conv_ms5837.py```.

## Author

**Olivier den Ouden** - *KNMI* - [HFSP SeabirdSound](https://seabirdsound.org)
