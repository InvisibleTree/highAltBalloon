import os
import time
import argparse
from datetime import datetime 
from Adafruit_BMP085 import BMP085

bmp = BMP085(0x77)

#Create logging files 
#!!OVERWRITES ANY OLD FILES THERE!! 
#TODO Sort logs by date created?
pressureF = open('../../logs/pressurelog.txt', 'w')
altF = open('../../logs/altLog.txt', 'w')

#Check command line arguments for parameters
parser = argparse.ArgumentParser(description='Log surrounding temp.')
parser.add_argument("-s" "--seconds", type=int, dest="seconds", help="Number of seconds between logs")
args = parser.parse_args()
seconds = args.seconds

#Set interval to instructed value.
if seconds:
	interval = seconds
else:
	interval = input("Enter logging interval (seconds): ")

#Define time variables
while True:
	d = datetime.now()
	year = "%02d" % (d.year)
	month = "%02d" % (d.month)
	day = "%02d" % (d.day)
	hour = "%02d" % (d.hour)
	min = "%02d" % (d.minute)
	sec = "%02d" % (d.second)

#Write to log files
	pressureF.write(str(day) + '/' + str(month) + '/' + str(year) + ' ' + str(hour) + ':' + str(min) + ':' + str(sec) + ' = ' + str(bmp.readPressure()) + 'Pa\n')
	altF.write(str(day) + '/' + str(month) + '/' + str(year) + ' ' + str(hour) + ':' + str(min) + ':' + str(sec) + ' = ' + str(bmp.readAltitude()) + 'm\n')
	time.sleep(int(interval))

