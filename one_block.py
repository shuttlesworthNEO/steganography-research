import time
import numpy as np
import math
import random

start_time = time.time()
input=''
def gen_key(x):
	outKey=""

	f=open("key.txt",'w')

	for i in range(0,x/88+1):
		color_key = random.randint(0,256)
		angle_key = random.randint(0,360)
		dist_key = random.randint(0,16)
		outKey = outKey + str(format(color_key,'02X')) + " " + str(format(angle_key,'03X')) + " " +str(format(dist_key,'1X'))
		#if(i != x/88):
		outKey = outKey + ' '

	f.write(outKey)
	f.close()

i = open("test.txt",'r')
input = i.read()

if(len(input)%4!=0):
	if(len(input)%4==1):
		input +="000"
	elif(len(input)%4==2):
		input +="00"
	elif(len(input)%4==3):
		input +="0"

gen_key(len(input))

#---------------------KEY TO BE USED------------------
f=open("key.txt",'r')     #obtaining keys and putting them in 'key' named list
key=f.read().split(' ')
f.close()

#----------------MATRIX INITIALIZATION-----------------
B = np.zeros((0,3)) #Matrix with x-y coordinates without encryption
C = np.zeros((0,3)) #Matrix with angle and distance without encryption
D = np.zeros((0,3)) #Matrix with angle and distance after encryption
E = np.zeros((0,3)) #Matrix with x-y coordinates after encryption
k=0
#------------------------------------------------------
input_counter = 0
angle_counter = 0
center_x = 76
center_y = 76

#------------FUNCTION TO CALCULATE X-Y COORDINATES-----
def plot_pixel():
	global input_counter
	global angle_counter
	global center_x
	global center_y
	global B
	global C
	global D
	global E
	global a
	global k
	
	# input values from text file
	color = ""
	color = input[input_counter]
	color += input[input_counter+1]
	color = int(color,16)
	angle = int(input[input_counter+3],16)	   
	dist = int(input[input_counter+2],16)
	
	
	# set value of angle
	if angle_counter>344:
		angle_counter = 0
		center_x += 152
		
	if center_x>=1520:
		center_x = 76
		center_y += 152
		
	angle = np.float64(angle_counter) + angle
	angle_counter += 16.0
	
	
	# calculte x-y coordinates without encryption
	x = (np.float64(58.0+dist))*math.cos(math.radians(angle))
	y = (np.float64(58.0+dist))*math.sin(math.radians(angle))
	
	x = np.float64(center_x) + x
	y = np.float64(center_y) + y
	
	B = np.append(B,[[color,x,y]],axis=0)
	C = np.append(C,[[color,angle,dist]],axis=0)
	
	
	# ENCRYPTION PROCESS
	color_key = int(key[(3*(k/22))],16)
	angle_key = int(key[3*(k/22) + 1],16)
	dist_key = int(key[3*(k/22) + 2],16)
	
	new_color = color^color_key
	new_angle = (angle+angle_key)%360
	new_dist = (dist + dist_key)%16
	
	D = np.append(D,[[new_color,new_angle,new_dist]],axis=0)
	
	# calculate x-y coordinates with encryption
	x = (np.float64(58.0+new_dist))*math.cos(math.radians(new_angle))
	y = (np.float64(58.0+new_dist))*math.sin(math.radians(new_angle))
	
	x = np.float64(center_x) + x
	y = np.float64(center_y) + y
	
	E = np.append(E,[[new_color,x,y]],axis=0)
		
	k=k+1
	
	   
def fill_block():
	global input_counter
	plot_pixel()
	input_counter += 4

	
def execute():
	global input_counter
	while(input_counter<len(input)-1):
		fill_block()


execute()

print "\n------------ B -------------"
print "color		X		Y"
print B

print "\n------------ C -------------"
print "color	Ang	Dist"
print C

print "\n------------ D -------------"
print "newC	newA	newD"
print D

print "\n------------ E -------------"
print "newC		newX		newY"
print E

print("--- %s seconds ---" % (time.time() - start_time))
# write E to output file with one decimal precision
mat = np.matrix(E)
with open('outfile.txt','wb') as f:
	for line in mat:
		np.savetxt(f, line, fmt='%.1f', delimiter=' ', newline='\n')