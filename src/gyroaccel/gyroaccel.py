#!/usr/bin/python
import argparse
import smbus
import time
import math
from datetime import datetime

# Power management registers 
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
	# little-endian structure so convert 2c words from 2's a compliment
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
address = 0x68 # i2c address of MPU-6050

#wake up 6050 
bus.write_byte_data(address, power_mgmt_1, 0)

#create logs
logTime = datetime.now().strftime("%Y.%m.%d-%H:%M:%S")

logGyro = "GYRO-" + logTime + ".log"
logAccel = "ACCEL-" + logTime + ".log"
logGLGyro = "GLGYRO-" + logTime + ".log"
logGLAccel = "GLACCEL-" + logTime + ".log"

gyroF = open('../../logs/' + logGyro, 'w')
accelF = open('../../logs/' + logAccel, 'w')
GLgyroF = open('../../logs/' + logGLGyro, 'w')
GLaccelF = open('../../logs/' + logGLAccel, 'w')

# init argparse
parser = argparse.ArgumentParser(description='Log surrounding gyro/accel.')
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

	# human readable log
	gyroF.write(str(day) + '/' + str(month) + '/' + str(year) + ' ' + str(hour) + ':' + str(min) + ':' + str(sec) + ' = ' + ' x: ' + str(gyro_xout_scaled) + ' y: ' + str(gyro_yout_scaled) + ' z: ' + str(gyro_zout_scaled) + ' degrees per second\n')
	accelF.write(str(day) + '/' + str(month) + '/' + str(year) + ' ' + str(hour) + ':' + str(min) + ':' + str(sec) + ' = ' + ' x: ' + str(accel_xout_scaled) + ' y: ' + str(accel_yout_scaled) + ' z: ' + str(accel_zout_scaled) + ' m s^-2\n')

	# openGL log
	GLaccelF.write(str(get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled))+" "+str(get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)))
	
	time.sleep(int(interval))
