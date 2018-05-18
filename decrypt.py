import sys
import cv2
import numpy as np
import math
import matplotlib.pyplot as plt

arguments = sys.argv
input_image = arguments[1]

image = plt.imread(input_image)
image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)

input_counter = 0
angle_counter = 0
center_x = 76 #75 0 Indexing
center_y = 76

output_data = ''

complete_flag = False

def rgb_to_hex(x):
	return '%02x%02x%02x' % (x[0], x[1], x[2])


#Function to calculate magnitude
def mag(x,y):
	ret = np.float64(x*x + y*y)
	ret = math.sqrt(ret)
	
	return ret

#Function to calculate original values
def get_this(x,y):
	x = x%152
	center_x_dec = 76.00000000
	x = x - center_x_dec
	
	y = y%152
	center_y_dec = 76.00000000
	y = y - center_y_dec
	
	dist = mag(x,y)
	
	angle = math.atan2(y,x)
	if angle < 0:
		angle = angle + 2*math.pi
	angle = math.degrees(angle)
	
	
	dist = round(dist)
	dist = dist - 58
	angle = round(angle)
	
	# # calculate original values
	# angle_key = int(key[3*(ind/22) + 1],16)
	# dist_key = int(key[3*(ind/22) + 2],16)
	
	# angle = (angle-angle_key)%360
	# dist = dist - dist_key
	
	# ind = ind+1
	
	return {'distance' : dist, 'angle': angle}

def get_pixel(a, b):
	global input_counter
	global angle_counter
	global center_x
	global center_y
	
	dist = b
	angle = a
	
	# set value of angle
	if angle_counter>344:
		angle_counter = 0
		center_y += 152
		
	if center_y>=1520:
		center_y = 76
		center_x += 152
		
	angle = np.float64(angle_counter) + angle	
	
	# calculte x-y coordinates without encryption
	x = (np.float64(58.0+dist))*math.cos(math.radians(angle))
	y = (np.float64(58.0+dist))*math.sin(math.radians(angle))
	
	x = np.float64(center_x) + x
	y = np.float64(center_y) + y

	return int(math.ceil(x)), int(math.ceil(y))


def calc_binary(x):
	my_hexdata = x
	scale = 16 ## equals to hexadecimal
	num_of_bits = 4
	return str(bin(int(my_hexdata, scale))[2:].zfill(num_of_bits))

def get_error_val(x):
	bits = {
		'00' : 0,
		'11' : 1,
		'01' : -1
	}

	return bits[x]

def decrypt(angle, distance, color):
	global output_data
	index = len(color) - 1
	zero = calc_binary(color[index])
	error = calc_binary(color[index-1])
	if zero == calc_binary('F'):
		distance = '{:x}'.format(distance - get_error_val(zero[0:2]))
		output_data += distance
	else:
		# print angle, distance, 'angle and distance'
		# angle = angle
		# distance = distance - get_error_val(error[0:2])
		# print angle, distance, 'angle and distance after'
		angle = '{:x}'.format(angle%16)
		distance = '{:x}'.format(distance%16)
		temp = color[0:index-1]

		zero_str = ''
		zero_count = int(color[index], 16)

		for i in range(0, zero_count):
			zero_str += '0'

		output_data += distance + angle + zero_str + temp 

if __name__ == '__main__':
	#Iterating over each 10x10 grid along rows

	for x in range(0,10):
		for y in range(0,10):
			box = image[y*152: 152 + y*152, x*152: 152 + x*152]
			# Calculating index for start and end color
			x_index = 150 + x*152
			y_index = 151 + y*152

			
			start = box[151, 150]
			end = box[151, 151]

			start_val = int(rgb_to_hex(start), 16)
			end_val = int(rgb_to_hex(end), 16)
			if start_val == end_val:
				print 'Decryption Completed'
				complete_flag = True
				print output_data
				break
			else:
				while angle_counter <= 344:
					angle_flag = True
					for a in range(0, 16):
						if angle_flag:
							for b in range(0, 16):
								x_data, y_data = get_pixel(a, b)
								val = int(rgb_to_hex(box[y_data, x_data]), 16)
								if val >= start_val+1 and val <= end_val - 1:
									temp_str = '{:x}'.format(val - (start_val + 1))
									decrypt(a, b, temp_str)
									angle_counter += 16.0
									angle_flag = False
									break

					if angle_flag:
						angle_counter += 16.0	

		
		if complete_flag:
			break		
