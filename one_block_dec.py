import numpy as np
import math

output = ''   # final output 

#---------------------KEY TO BE USED------------------
f=open("key.txt",'r')     #obtaining keys and putting them in 'key' named list
key=f.read().split(' ')
f.close()
print key

f=open("output.txt",'w') # now open the output file to write hex file

fname = open("outfile.txt",'r')
mat = np.loadtxt(fname, delimiter=' ')
fname.close()

#----------------MATRIX INITIALIZATION-----------------
D = np.zeros((0,3)) #Matrix with angle and distance after encryption
C = np.zeros((0,3)) #Matrix with angle and distance without encryption
ind = 0


#--------FUNCTION TO CALCULATE DISTANCE---------------
def mag(x,y):
	ret = np.float64(x*x + y*y)
	ret = math.sqrt(ret)
	
	return ret


#--------FUNCTION TO DECRYPT--------------------------
def get_this(k,x,y):
	global ind
	global C
	global D
	color = k
	
	x = x%152
	center_x = 76.00000000
	x = x - center_x
	
	y = y%152
	center_y = 76.00000000
	y = y - center_y
	
	dist = mag(x,y)
	
	angle = math.atan2(y,x)
	if angle < 0:
		angle = angle + 2*math.pi
	angle = math.degrees(angle)
	
	
	dist = round(dist)
	dist = dist - 58
	angle = round(angle)
	
	D = np.append(D,[[color,angle,dist]],axis=0)
	
	
	# calculate original values
	color_key = int(key[3*(ind/22)],16)
	angle_key = int(key[3*(ind/22) + 1],16)
	dist_key = int(key[3*(ind/22) + 2],16)
	
	angle = (angle-angle_key)%360
	new_color = int(k)^color_key
	dist = dist - dist_key
	
	ind = ind+1
	
	return [dist,angle,new_color]

	
def execute():		
	global output
	global input
	global C
	i=0
	
	for line in mat:	
		r = get_this(line[0],line[1],line[2])			
		stri = ""
		dist=int(r[0])
		ang=int(r[1])
		color=int(r[2])
		dist = dist%16
		
		C = np.append(C,[[color,ang,dist]],axis=0)
		i+=1
		
		ang = ang%16
		
		stri = stri + str(format(color,'02X'))
		stri = stri + str(format(dist,'1X'))
		stri = stri + str(format(ang,'1X'))

		output = output + stri
	
	print "\n------------ D -------------"
	print "newC	newA	newD"
	print D
	
	print "\n------------ C -------------"
	print "color	Ang	Dist"
	print C


execute()

f.write(output)
f.close()