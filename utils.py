import cv2
import numpy as np
import hilbert


image = cv2.imread('image.jpg')

image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


def max_range(colors):
	difference = -1
	start = 0
	end = 0
	for x, i in enumerate(colors):	
		if i < len(colors):
			if colors[i] - colors[i-1] > difference:
				start = i-1
				end = i
				difference = colors[i] - colors[i-1]
	return colors[start], colors[end], difference

#Iterating over each 10x10 grid along rows
for x in range(0,10):
	for y in range(0,10):
		box = image[y*152: 152 + y*152, x*152: 152 + x*152]
		unique_colors = np.unique(box.reshape(-1, box.shape[2]), axis=0).tolist()
		#Reducing 3D array to 1D array using Hilbet's algorithm
		colours_one_d = [hilbert.Hilbert_to_int(color) for color in unique_colors ]
		# print colours_one
		colours_one_d.sort()

		#Finding the colors with maximum range between them
		start, end, count = max_range(colours_one_d)
		print count, "count"
		#Converting back to RGB
		start_rgb = hilbert.int_to_Hilbert(start, 3)
		end_rgb = hilbert.int_to_Hilbert(end, 3)

		#Calculating index for hiding start and end color
		x_index = 151 + x*152
		y_index = 150 + y*152
		image[y_index, x_index] = start_rgb
		image[y_index+1, x_index] = end_rgb
		
		# #Converting RGB to Hexadecimal Values
		# start = '#%02x%02x%02x' % (start_rgb[0], start_rgb[1], start_rgb[2])
		# end = '#%02x%02x%02x' % (end_rgb[0], end_rgb[1], end_rgb[2])

		#Adding data to the color in range
		string = 'ffffffffffffffffffffffffffffffffffffff'
		temp = string
		color = start
		print color, 'start'

		for c in temp:
			if int(c, 16) + color < end:
				color = int(c, 16) + color
				string = string[1:]
			else:
				break
		print hilbert.int_to_Hilbert(color, 3), "rbg"
		print string
		# temp = unique_colors.sort(key=lambda (r,g,b):hilbert.Hilbert_to_int([r, g, b]))
		# print unique_colors
