#!/usr/bin/python
# import some libraries
import os
import time
import argparse

# get params from user
# TODO change this to a more automatic form:
# 1. check args
# 2. no -s? ask for interval
# 3. no --weight or --height? default to max size
# 4. no save folder (-sf)? default to local ~/pictures/picam

parser = argparse.ArgumentParser(description='Log surrounding temp.')
parser.add_argument("-s" "--seconds", type=int, dest="seconds", help="Number of seconds between images")
parser.add_argument("--width", type=int, dest="width", help="Saved image width")
parser.add_argument("--height", type=int, dest="height", help="Saved image height")
parser.add_argument("-SF" "--savefolder", dest="saveFolder", help="Name of folder to save images")
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
if args.saveFolder:
	saveFolder = args.saveFolder
else:
	saveFolder = "images"

#saveFolder = input("Enter folder name to save images to: ")
#imgWidth = input("\nEnter image width (max 2592): ")
#imgHeight = input("\nEnter image height (max 1944): ")

# incrementing  numerical suffix added to each image
fileIncr = 1

# create save dir
while os.path.isdir("../../logs/" + str(saveFolder)) == False:
	os.mkdir('../../logs/' + str(saveFolder))
saveFolder = '../../logs/' + str(saveFolder)
# loop infinitely
while True:

	# set fileIncrNo to 000X where x is fileIncr
	fileIncrNo = "%04d" % (fileIncr)

	print("\n---Saving image " + str(fileIncr) +  "---")
	

	# capture the image using raspistill - Has sharpening, auto white balance and average metering mode
	os.system("raspistill -w " + str(imgWidth) + " -h " + str(imgHeight) + " -o " + str(saveFolder) + "/" + "image_" + str(fileIncrNo) + ".jpg -sh 40 -awb auto -mm average -v")
	
	# increment file 
	fileIncr += 1

	# wait chosen interval
	time.sleep(interval)

# just in case
else:
	print("\n ---Inactive--\n")
 
