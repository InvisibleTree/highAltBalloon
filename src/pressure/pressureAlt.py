import os
import time
import argparse
from datetime import datetime 
from Adafruit_BMP085 import BMP085

bmp = BMP085(0x77)

# Create logging files 
logTime = datetime.now().strftime("%Y.%m.%d-%H:%M:%S")

logPressure = "PRESSURE-" + logTime + ".log"
pressureF = open('../../logs/' + logPressure, 'w')
pressureF.close()

logAlt = "ALTITUDE-" + logTime + ".log"
altF = open('../../logs/' + logAlt, 'w')
altF.close()

# Check command line arguments for parameters
parser = argparse.ArgumentParser(description='Log surrounding temp.')
parser.add_argument("-s" "--seconds", type=int, dest="seconds", help="Number of seconds between logs")
args = parser.parse_args()
seconds = args.seconds

# set interval to instructed value.
if seconds:
	interval = seconds
else:
	interval = input("Enter logging interval (seconds): ")


while True:
	# define time variables
	d = datetime.now()
	year = "%02d" % (d.year)
	month = "%02d" % (d.month)
	day = "%02d" % (d.day)
	hour = "%02d" % (d.hour)
	min = "%02d" % (d.minute)
	sec = "%02d" % (d.second)

	# write to log files
	pressureF = open('../../logs/' + logPressure, 'a')
	pressureF.write(str(day) + '/' + str(month) + '/' + str(year) + ' ' + str(hour) + ':' + str(min) + ':' + str(sec) + ' = ' + str(bmp.readPressure()) + 'Pa\n')
	pressureF.close

	altF = open('../../logs/' + logAlt, 'a')
	altF.write(str(day) + '/' + str(month) + '/' + str(year) + ' ' + str(hour) + ':' + str(min) + ':' + str(sec) + ' = ' + str(bmp.readAltitude()) + 'm\n')
	altF.close()

	time.sleep(int(interval))

