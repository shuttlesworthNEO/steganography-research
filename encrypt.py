import sys
import cv2
import numpy as np
import math
import matplotlib.pyplot as plt
import webcolors

arguments = sys.argv
data = arguments[1]
input_image = arguments[2]
output_image = arguments[3]

image = plt.imread(input_image)
image.setflags(write=1)

# print image.shape, 'shape'

# print image[0, 0], '00'
# print image[1,1], '11'

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
	

	dist = int(round(dist))
	dist = dist - 58
	if int((angle_counter-16)) > 0:
		angle = int(round(angle)) % int((angle_counter-16))
	else:
		angle = int(round(angle))
	# print angle_counter, 'here mf'
	# # calculate original values
	# angle_key = int(key[3*(ind/22) + 1],16)
	# dist_key = int(key[3*(ind/22) + 2],16)
	
	# angle = (angle-angle_key)%360
	# dist = dist - dist_key
	
	# ind = ind+1
	
	return {'distance' : dist, 'angle': angle}

def calculate_error(x, y, values):
	# print values
	calculated_values = get_this(x, y)
	# print calculated_values
	distance = int(calculated_values['angle'] - values['angle'])
	angle = int(calculated_values['angle'] - values['angle'])
	if angle == -15:
		angle = -1

	if distance == -15:
		distance = -1

	return {
		'distance' : distance,
		'angle' : angle,
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

	if flag:
		if input_counter == len(data)-1:
			angle = int('F', 16)
			dist = int(data[input_counter],16)
			input_counter += 1
		elif input_counter < len(data)-1:
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
			center_y += 152
			
		if center_y>=1520:
			center_y = 76
			center_x += 152
			
		angle = np.float64(angle_counter) + angle
		angle_counter += 16.0
		
		
		# calculte x-y coordinates without encryption
		x = (np.float64(58.0+dist))*math.cos(math.radians(angle))
		y = (np.float64(58.0+dist))*math.sin(math.radians(angle))
		
		x = np.float64(center_x) + x
		y = np.float64(center_y) + y

		error = calculate_error(int(math.ceil(x)), int(math.ceil(y)), original_values)
		return math.ceil(x), math.ceil(y), error
	else:
		if angle_counter>344:
			angle_counter = 0
			center_y += 152
			
		if center_y>=1520:
			center_y = 76
			center_x += 152

		# print center_y, center_x, angle_counter	


def max_range(colors):
	difference = -1
	start = 0
	end = 0
	for i, x in enumerate(colors):
		if i < len(colors) - 1:
			if colors[i+1] - colors[i] > difference:
				start = i
				end = i + 1
				difference = colors[i+1] - colors[i]
	return colors[start], colors[end], difference



def calculate_error_char(values):
	error_str = ''
	bits = {
		0 : '00',
		1 : '11',
		-1 : '01'
	}
	for k, v in values.iteritems():
		#Distance being added to the string before angle
		error_str += bits[values[k]]

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
		equal = False
		for y in range(0,10):
			if flag:
				#Selecting a box of size 152x152
				box = image[y*152: 152 + y*152, x*152: 152 + x*152]

				#Finding a list of unique pixel RGB values
				unique_colors = np.unique(box.reshape(-1, box.shape[2]), axis=0).tolist()
				
				#Convert RGB values to int for sorting
				unique_colors = [int(rgb_to_hex(t), 16) for t in unique_colors]
				
				#Sort the values for finding maximum range
				unique_colors.sort()

				#Finding the colors with maximum range between them
				start, end, count = max_range(unique_colors)

				# Converting colour back to hex
				start = '{:x}'.format(start)
				end = '{:x}'.format(end)

				
				#Calculating index for hiding start and end color
				x_index = 150 + x*152
				y_index = 151 + y*152
				
				#Adding the start and end colour
				image[y_index, x_index] = webcolors.hex_to_rgb('#'+start)
				image[y_index, x_index+1] = webcolors.hex_to_rgb('#'+end)



				#Adding data to the color in range
				while angle_counter <= 344 and flag:
					#Find index and error for the data to be crypted
					x_index, y_index, error = plot_pixel()

					#Finding the error character
					error_char = calculate_error_char(error)
					
					#Initialising the colour to start + 1
					color = '{:x}'.format(int(start, 16) + 1)

					#Intitialising the final colour to end - 1
					color_end = '{:x}'.format(int(end, 16) - 1)


					if input_counter == len(data):
						zero_count = 15
						zero_char = '{:x}'.format(zero_count)

						#First appending the error char and then the zero char
						#If zero char is 'F', then angle = 'F'
						sten_data = error_char + zero_char
						color = sum_hex(color, sten_data)
					else:
						zero_count = 0
						while data[input_counter] == '0' and input_counter < len(data) and zero_count < 15:
								zero_count += 1
								input_counter += 1
								if input_counter == len(data):
									break

						zero_char = '{:x}'.format(zero_count)

						sten_data = error_char + zero_char

						if input_counter < len(data):
							if data[input_counter] == '0':
								if int(sum_hex(color, sten_data), 16) <= int(end, 16):
									color = sum_hex(color, sten_data)
								else:
									print 'This image cannot be Steganographed'
							else:
								i = 3
								if input_counter+i >= len(data):
									i = 3 - (input_counter + i - len(data) + 1)

							while i >= 0:
								temp = sten_data
								temp = data[input_counter : input_counter+i] + temp
								if int(sum_hex(color, temp), 16) <= int(end, 16):
									sten_data = temp
									break
								else:
									i -= 1
							
							color = sum_hex(color, sten_data)
							input_counter += i
								# print color, end
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
					image[int(y_index), int(x_index)] = color
					
					if input_counter >= len(data)-1:
						print "Steganography Completed"
						flag = False
						plot_pixel()

			else:
				image[151 + y*152, 151 + x*152] = image[151 + y*152, 150 + x*152]
				
				equal = True
				break
		if equal:
			break		# print image[151 + y*152, 151 + x*152], image[151 + y*152, 150 + x*152]
				# angle_counter = 360
				# plot_pixel()
	if flag:
		print "The complete string could not be encrypted."
		remaining = data[input_counter: len(data)]
		print "The remaining string is ", remaining	


	
	# image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
	# print 'before saving'
	# print image[0, 0], '00'
	# print image[1,1], '11'
	# cv2.imwrite(output_image, image)   
	plt.imsave(fname = output_image, arr = image, format = 'png')       


				# temp = unique_colors.sort(key=lambda (r,g,b):hilbert.Hilbert_to_int([r, g, b]))
				# print unique_colors
