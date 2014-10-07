#!/usr/bin/python
# import some libraries
import os
import time
import argparse
from datetime import datetime

# get params from user
# TODO change this to a more automatic form:
# rewrite in brainfuck

parser = argparse.ArgumentParser(description='Log surrounding temp.')
parser.add_argument("-s" "--seconds", type=int, dest="seconds", help="Number of seconds between images")
parser.add_argument("--width", type=int, dest="width", help="Saved image width")
parser.add_argument("--height", type=int, dest="height", help="Saved image height")
parser.add_argument("--savefolder" "-SF", dest="photoLoc", help="Location of photos")
args = parser.parse_args()

if args.seconds:
	interval = args.seconds
else:
	interval = int(input("Enter interval between images (seconds): "))
if args.width:
	imgWidth = args.width
else:
	imgWidth = 2592
if args.height:
	imgHeight = args.height
else:
	imgHeight = 1944
if args.photoLoc:
	photos = args.photoLoc
else:
	photos = "photos"
#saveFolder = input("Enter folder name to save images to: ")
#imgWidth = input("\nEnter image width (max 2592): ")
#imgHeight = input("\nEnter image height (max 1944): ")


# create save dir
while os.path.isdir("../../logs/" + str(photos)) == False:
	os.mkdir('../../logs/' + str(photos))
saveFolder = '../../logs/' + str(photos)
# loop infinitely
while True:

	# define time variables
	d = datetime.now()
	year = "%02d" % (d.year)
	month = "%02d" % (d.month)
	day = "%02d" % (d.day)
	hour = "%02d" % (d.hour)
	min = "%02d" % (d.minute)
	sec = "%02d" % (d.second)

	# capture the image using raspistill - Has sharpening, auto white balance and average metering mode
	os.system("raspistill -w " + str(imgWidth) + " -h " + str(imgHeight) + " -o " + str(saveFolder) + "/" + (str(day) + '-' + str(month) + '-' + str(year) + '_' + str(hour) + ':' + str(min) + ':' + str(sec)) + ".jpg -sh 40 -awb auto -mm average -v")

	time.sleep(int(interval))

# just in case
else:
	print("\n NOBODY CAN HEAR ME IN SPACE!\n")
 
