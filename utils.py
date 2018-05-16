import sys
import cv2
import numpy as np
import hilbert
import math

arguments = sys.argv
data = arguments[1]
input_image = arguments[2]
output_image = arguments[3]

image = cv2.imread(input_image)
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

input_counter = 0
angle_counter = 0
center_x = 76 #75 0 Indexing
center_y = 76

flag = True


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

def calculate_error(x, y, values):
	print x, y
	calculated_values = get_this(x, y)
	print calculated_values, 'calculated_values', values, 'original_values'
	return {
		'distance' : calculated_values['distance'] - values['distance'],
		'angle' : (calculated_values['angle'] - values['angle']) % 16
	}

def plot_pixel():
	global input_counter
	global angle_counter
	global center_x
	global center_y
	
	# input values from text file
	# color = ""
	# color = input[input_counter]
	# color += input[input_counter+1]
	# color = int(color,16)

	if input_counter + 1 == len(data):
		angle = int('F', 16)
		dist = int(data[input_counter],16)
		input_counter += 1
	else:
		angle = int(data[input_counter+1],16)	   
		dist = int(data[input_counter],16)
		input_counter += 2

	original_values = {
		'distance' : dist,
		'angle' : angle
	}
	
	
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

	print original_values, 'original_values', x, y
	error = calculate_error(int(math.ceil(x)), int(math.ceil(y)), original_values)
	return int(math.ceil(x)), int(math.ceil(y)), error
	


def max_range(colors):
	difference = -1
	start = 0
	end = 0
	for i, x in enumerate(colors):
		if i < len(colors):
			if int(rgb_to_hex(colors[i]), 16) - int(rgb_to_hex(colors[i-1]), 16) > difference:
				start = i-1
				end = i
				difference = int(rgb_to_hex(colors[i]), 16) - int(rgb_to_hex(colors[i-1]), 16)
	return colors[start], colors[end], difference



def calculate_error_char(values):
	error_str = ''
	bits = {
		0 : '00',
		1 : '11',
		-1 : '01'
	}
	print values
	for k, v in values.iteritems():
		print k, v
		error_str += bits[v]

	return '{:x}'.format(int(error_str, 2))


def sum_hex(a, b):
	a = int(a, 16)
	b = int(b, 16)

	sum = a + b

	return '{:x}'.format(sum).upper()

def hex_to_rgb(value):
    lv = len(value)
    return list(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

# def toBinary(n):
#     return ''.join(str(1 & int(n) >> i) for i in range(8)[::-1])


if __name__ == '__main__':
	#Iterating over each 10x10 grid along rows
	for x in range(0,10):
		if flag:
			for y in range(0,10):
				if flag:
					box = image[y*152: 152 + y*152, x*152: 152 + x*152]
					unique_colors = np.unique(box.reshape(-1, box.shape[2]), axis=0).tolist()
					# #Reducing 3D array to 1D array using Hilbet's algorithm
					# colours_one_d = [hilbert.Hilbert_to_int(color) for color in unique_colors ]
					# # print colours_one
					# colours_one_d.sort()
					unique_colors.sort()
					#Finding the colors with maximum range between them
					start, end, count = max_range(unique_colors)

					#Calculating index for hiding start and end color
					x_index = 151 + x*152
					y_index = 150 + y*152
					image[y_index, x_index] = start
					image[y_index+1, x_index] = end
					
					#Converting RGB to Hexadecimal Values
					start_hex = rgb_to_hex(start)
					end_hex = rgb_to_hex(end)


					#Adding data to the color in range
					while angle_counter <= 344 and flag:
						x_index, y_index, error = plot_pixel()
						error_char = calculate_error_char(error)
						color = start_hex
						
						if input_counter == len(data):
							zero_count = 15
							zero_char = '{:x}'.format(zero_count)

							sten_data = error_char + zero_char
							color = sum_hex(color, sten_data)
						else:
							zero_count = 0
							while data[input_counter] == '0' and input_counter < len(data)-1 and zero_count < 15:
									zero_count += 1
									input_counter += 1

							zero_char = '{:x}'.format(zero_count)

							sten_data = ''
							
							if data[input_counter] == '0':
								sten_data = error_char + zero_char
								color = sum_hex(color, sten_data)
							else:
								i = 4
								while input_counter + i >= len(data):
									i -= 1

								while i >= 0:
									sten_data = data[input_counter : input_counter+i] + error_char + zero_char
									print sten_data
									if int(sum_hex(color, sten_data), 16) < int(end_hex, 16):
										break
									else:
										i -= 1
								color = sum_hex(color, sten_data)
								input_counter += i

						# if sum_hex(color, sten_data) < end:
						# 	color += sten_data
						# else:


						# while input_counter < len(data)-1:
						# 	if sum_hex(color, data[input_counter+1]) < end:
						# 		color = sum_hex(color, data[input_counter+1])
						# 		input_counter += 1
						# 	else:
						# 		break

						# for c in temp:
						# 	if int(c, 16) + color < end:
						# 		color = int(c, 16) + color
						# 		string = string[1:]
						# 	else:
						# 		break
						color = hex_to_rgb(color)
						image[x_index, y_index] = color

						if input_counter >= len(data):
							print "Steganography Completed"
							flag = False
		else:
			break

	image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
	cv2.imwrite(output_image, image)           

				# temp = unique_colors.sort(key=lambda (r,g,b):hilbert.Hilbert_to_int([r, g, b]))
				# print unique_colors
