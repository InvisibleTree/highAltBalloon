#!/usr/bin/python
# import some libraries
import os
import time

# get params from user
saveFolder = input("Enter folder name to save images to: ")
imgWidth = input("\nEnter image width (max 2592): ")
imgHeight = input("\nEnter image height (max 1944): ")
interval = int(input("\nEnter interval between images (seconds): \n"))

# incrementing  numerical suffix added to each image
fileIncr = 1

# create save dir

os.mkdir(str(saveFolder))
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
 
