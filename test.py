import random

colours_length = 1000
colours = []
for i in range(1, colours_length):
	colours.append (
		[
			random.random(),
			random.random(),
			random.random()
		]
	)

print colours