# for initial placement, I don't think it's very necessary to define a new class. 
# use a seperate module is clean enough

import random, math
import block_occupation

'''
I use occupation grid (the matrix) to present and check if the unit grid is available or
if it is already occupied. The grid (x, y) represent a unit square centered at (x,y) 
(area from [x-0.5, x+0.5] * [y-0.5, y+0.5])
'''

def slide_x_direction(grid, granularity, xx, yy, width, height):
	while check_row_occupation(grid, granularity, xx-granularity, yy, width, height):
		xx -= granularity
	return xx

def slide_y_direction(grid, granularity, xx, yy, width, height):
	while check_col_occupation(grid, granularity, xx, yy-granularity, width, height):
		yy -= granularity
	return yy

def init_place_random(intp_size, granularity, chiplet_count, width, height):
	x, y, rotation = [0] * chiplet_count, [0] * chiplet_count, [0] * chiplet_count
	pass

def init_place_tight(intp_size, granularity, chiplet_count, width, height):
	x, y, rotation = [0] * chiplet_count, [0] * chiplet_count, [0] * chiplet_count	
	grid = block_occupation.initialize_grid(int(intp_size/granularity))
	# print_grid(grid)
	# print (width)
	# print (height)
	for i in range(chiplet_count):
		xx, yy = int((intp_size - 0.5 - width[i] / 2)/granularity)*granularity, int((intp_size -0.5 - height[i] / 2)/granularity)*granularity
		# xx, yy = (int(intp_size/granularity) - int(width[i]/2/granularity+0.49)) * granularity
		# print ('chiplet -', i, xx, yy,)
		if block_occupation.check_block_occupation(grid, granularity, xx, yy, width[i], height[i]) == False:
			print ('can\'t find tightly arraged initial placement')
			exit()
		xx = slide_x_direction(grid, granularity, xx, yy, width[i], height[i])
		yy = slide_y_direction(grid, granularity, xx, yy, width[i], height[i])
		# print ('slide to ', xx, yy)
		grid = block_occupation.set_block_occupation(grid, granularity, xx, yy, width[i], height[i], i)
		x[i], y[i] = xx, yy
	# for testing purpose, print the grid
	block_occupation.print_grid(grid)
	return x, y, rotation

