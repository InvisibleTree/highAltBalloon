# bring needed modules into program

import os
import time
import argparse
from datetime import datetime
from Adafruit_BMP085 import BMP085
import smbus
import math

bmp = BMP085(0x77) #PRESSURE

#Temp initialse
sensorFile = '/sys/bus/w1/devices/28-0000056e80cd/w1_slave'
def readTempRaw():
	f = open(sensorFile, 'r')
	lines = f.readlines()
	f.close()
	return lines
def readTemp():
	lines = readTempRaw()
	while lines[0].strip()[-3:] != 'YES':
		time.sleep(0.2)
		lines = readTempRaw()
	equalsPos = lines[1].find('t=')
	if equalsPos != -1:
		tempString = lines[1][equalsPos+2:]
		tempC = float(tempString)/1000.0
		return tempC

# GYRO-ACCEL Power management registers 
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

def read_byte(adr):
	return bus.read_byte_data(address, adr)

def read_word(adr):
	high = bus.read_byte_data(address, adr)
	low = bus.read_byte_data(address, adr+1)
	val = (high << 8) + low
	return val

def read_word_2c(adr):
	# GYRO-ACCEL little-endian structure so convert 2c words from 2's a compliment
	val = read_word(adr)
	if (val >= 0x8000):
		return -((66535 - val) + 1)
	else:
		return val

def dist(a,b):
	return math.sqrt((a*a) + (b*b))

def get_y_rotation(x,y,z):
	radians = math.atan2(x, dist(y,z))
	return -math.degrees(radians)

def get_x_rotation(x,y,z):
	radians = math.atan2(y, dist(x,z))
	return math.degrees(radians)

bus = smbus.SMBus(1)
address = 0x68 # GYRO-ACCEL i2c address of MPU-6050

#GYRO-ACCEL wake up 6050 
bus.write_byte_data(address, power_mgmt_1, 0)

#create logs
logTime = datetime.now().strftime("%Y.%m.%d-%H:%M:%S")

logGyro = "GYRO-" + logTime + ".log"
logAccel = "ACCEL-" + logTime + ".log"
logGLGyro = "GLGYRO-" + logTime + ".log"
logGLAccel = "GLACCEL-" + logTime + ".log"

logPressure = "PRESSURE-" + logTime + ".log"
logAlt = "ALTITUDE-" + logTime + ".log"

logTemp = "TEMP-" + logTime + ".log"


# open is only way to invoke O_CREAT as python is shit
gyroF = open('../../logs/' + logGyro, 'w').close()
accelF = open('../../logs/' + logAccel, 'w').close()
GLgyroF = open('../../logs/' + logGLGyro, 'w').close()
GLaccelF = open('../../logs/' + logGLAccel, 'w').close()

pressureF = open('../../logs/' + logPressure, 'w').close()
altF = open('../../logs/' + logAlt, 'w').close()

f = open('../../logs/' + logTemp, 'w').close()

# init argparse
parser = argparse.ArgumentParser(description='Log measurements')
parser.add_argument("-s" "--seconds", type=int, dest="seconds", help="Number of seconds between logs")
args = parser.parse_args()
seconds = args.seconds

if seconds:
	interval = seconds
else:
	interval = input("Enter logging interval (seconds): ")

while True:
	# read 16 bit raw data from accel and gyro registers 
	accel_xout = read_word_2c(0x3b)
	accel_yout = read_word_2c(0x3d)
	accel_zout = read_word_2c(0x3f)
 	
	gyro_xout = read_word_2c(0x43)
	gyro_yout = read_word_2c(0x45)
	gyro_zout = read_word_2c(0x47)

	# convert raw data to m s^-2 and degrees per second
	accel_xout_scaled = accel_xout / 16384.0 # from data sheet scale value is 16384.0
	accel_yout_scaled = accel_yout / 16384.0
	accel_zout_scaled = accel_zout / 16384.0

	gyro_xout_scaled = gyro_xout / 131 # from data sheet scale value is 131
	gyro_yout_scaled = gyro_yout / 131
	gyro_zout_scaled = gyro_zout / 131
	
	# init date values
	d = datetime.now()
	year = "%02d" % (d.year)
	month = "%02d" % (d.month)
	day = "%02d" % (d.day)
	hour = "%02d" % (d.hour)
	min = "%02d" % (d.minute)
	sec = "%02d" % (d.second)

	# open log files
	gyroF = open('../../logs/' + logGyro, 'a')
	accelF = open('../../logs/' + logAccel, 'a')
	GLgyroF = open('../../logs/' + logGLGyro, 'a')
	GLaccelF = open('../../logs/' + logGLAccel, 'a')

	# write to log -TEMP
	f = open('../../logs/' + logTemp, 'a')
	f.write(str(day) + '/' + str(month) + '/' + str(year) + ' ' + str(hour) + ':' + str(min) + ':' + str(sec) + ' = ' + str(readTemp()) + 'C\n')
	f.close
	time.sleep(int(interval))

	# write to log files - Pressure+Alt
	pressureF = open('../../logs/' + logPressure, 'a')
	pressureF.write(str(day) + '/' + str(month) + '/' + str(year) + ' ' + str(hour) + ':' + str(min) + ':' + str(sec) + ' = ' + str(round(bmp.readPressure())) + 'Pa\n')
	pressureF.close()
	altF = open('../../logs/' + logAlt, 'a')
	altF.write(str(day) + '/' + str(month) + '/' + str(year) + ' ' + str(hour) + ':' + str(min) + ':' + str(sec) + ' = ' + str(round(bmp.readAltitude())) + 'm\n')
	altF.close()

	# human readable log
	gyroF.write(str(day) + '/' + str(month) + '/' + str(year) + ' ' + str(hour) + ':' + str(min) + ':' + str(sec) + ' = ' + ' x: ' + str(gyro_xout_scaled) + ' y: ' + str(gyro_yout_scaled) + ' z: ' + str(gyro_zout_scaled) + ' degrees per second\n')
	accelF.write(str(day) + '/' + str(month) + '/' + str(year) + ' ' + str(hour) + ':' + str(min) + ':' + str(sec) + ' = ' + ' x: ' + str(accel_xout_scaled) + ' y: ' + str(accel_yout_scaled) + ' z: ' + str(accel_zout_scaled) + ' m s^-2\n')

	# openGL log
	GLaccelF.write(str(get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled))+" "+str(get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)))

	# close log files
	gyroF.close()
	accelF.close()
	GLgyroF.close()
	GLaccelF.close()

	# pause for given interval
	time.sleep(int(interval))
# just in case
else:
	print("Hey aliens!")
