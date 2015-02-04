# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import matplotlib.dates as md
import dateutil

# create empty dynamic arrays 
temp_x = []
x = []
y = []

f = open("temp.log", "r") # open log folder

for line in f: # load x and y values
	temp_line = line.split('=')
	temp_x.append(temp_line[0][:-1]) # trim spaces
	y.append(float(temp_line[1][1:-2])) # trim C
	
f.close()
x = [dateutil.parser.parse(s) for s in temp_x]

ax = plt.gca()
xfmt = md.DateFormatter('%d/%m/%Y %H:%M:%S')
ax.xaxis.set_major_formatter(xfmt)


plt.plot(x, y)

plt.title('Temprature against time')
plt.xlabel('Date and Time (DD/MM/YYYY HH:MM:SS)')
plt.ylabel('Temprature C')
plt.show()
