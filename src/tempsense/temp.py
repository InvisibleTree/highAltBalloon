# bring needed modules into program

import os
import time
import argparse
from datetime import datetime

# read from the sensor's output file
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

# create log files
logTime = datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
logTemp = "TEMP-" + logTime + ".log"
# open is only way to invoke O_CREAT as python is shit
f = open('../../logs/' + logTemp, 'w').close()

# check program arguments
parser = argparse.ArgumentParser(description='Log surrounding temp.')
parser.add_argument("-s" "--seconds", type=int, dest="seconds", help="Number of seconds between logs")
args = parser.parse_args()
seconds = args.seconds

if seconds:
	interval = seconds
else:
	interval = input("Enter logging interval (seconds): ")

while True:
	d = datetime.now()
	year = "%02d" % (d.year)
	month = "%02d" % (d.month)
	day = "%02d" % (d.day)
	hour = "%02d" % (d.hour)
	min = "%02d" % (d.minute)
	sec = "%02d" % (d.second)

	# write to log
	f = open('../../logs/' + logTemp, 'a')
	f.write(str(day) + '/' + str(month) + '/' + str(year) + ' ' + str(hour) + ':' + str(min) + ':' + str(sec) + ' = ' + str(readTemp()) + 'C\n')
	f.close
	time.sleep(int(interval))

# just in case
else:
	os.system('sudo fbi ../space.jpg')
