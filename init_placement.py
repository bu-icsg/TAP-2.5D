# for initial placement, I don't think it's very necessary to define a new class. 
# use a seperate module is clean enough

import random, math

'''
I use occupation grid (the matrix) to present and check if the unit grid is available or
if it is already occupied. The grid (x, y) represent a unit square centered at (x,y) 
(area from [x-0.5, x+0.5] * [y-0.5, y+0.5])
'''

def print_grid(grid):
	for i in grid:
		print (i)
	print

def initialize_grid(mi):
	grid = [[0 for _ in range(mi+1)] for _ in range(mi+1)]
	# boundary protection
	for i in range(mi+1):
		grid[0][i] = 1
		grid[mi][i] = 1
		grid[i][0] = 1
		grid[i][mi] = 1
	return grid

def check_block_occupation(grid, granularity, xx, yy, width, height):
	# print (int(xx/granularity)-int(width/2/granularity+0.49), int(xx/granularity)+int(width/2/granularity+0.49)+1)
	for i in range(int(xx/granularity)-int(width/2/granularity+0.49), int(xx/granularity)+int(width/2/granularity+0.49)+1):
		if (sum(grid[i][int(yy/granularity)-int(height/2/granularity+0.49):int(yy/granularity)+int(height/2/granularity+0.49)+1])):
			return False
	return True

def set_block_occupation(grid, granularity, xx, yy, width, height, chiplet_index):
	for i in range(int(xx/granularity)-int(width/2/granularity+0.49), int(xx/granularity)+int(width/2/granularity+0.49)+1):
		for j in range(int(yy/granularity)-int(height/2/granularity+0.49), int(yy/granularity)+int(height/2/granularity+0.49)+1):
			grid[i][j] = chiplet_index
	return grid

def check_row_occupation(grid, granularity, xx, yy, width, height):
	i = int(xx/granularity) - int(width/2/granularity+0.49)
	if i<=0:
		return False
	if (sum(grid[i][int(yy/granularity)-int(height/2/granularity+0.49):int(yy/granularity)+int(height/2/granularity+0.49)+1])):
		return False
	else:
		return True

def check_col_occupation(grid, granularity, xx, yy, width, height):
	j = int(yy/granularity) - int(height/2/granularity+0.49)
	if j<=0:
		return False
	for i in range(int(xx/granularity)-int(width/2/granularity+0.49), int(xx/granularity)+int(width/2/granularity+0.49)+1):
		if grid[i][j]:
			return False
	return True

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
	grid = initialize_grid(int(intp_size/granularity))
	# print_grid(grid)
	# print (width)
	# print (height)
	for i in range(chiplet_count):
		xx, yy = int((intp_size - 0.5 - width[i] / 2)/granularity)*granularity, int((intp_size -0.5 - height[i] / 2)/granularity)*granularity
		# xx, yy = (int(intp_size/granularity) - int(width[i]/2/granularity+0.49)) * granularity
		# print ('chiplet -', i, xx, yy,)
		if check_block_occupation(grid, granularity, xx, yy, width[i], height[i]) == False:
			print ('can\'t find tightly arraged initial placement')
			exit()
		xx = slide_x_direction(grid, granularity, xx, yy, width[i], height[i])
		yy = slide_y_direction(grid, granularity, xx, yy, width[i], height[i])
		# print ('slide to ', xx, yy)
		set_block_occupation(grid, granularity, xx, yy, width[i], height[i], i+1)
		# print_grid(grid)
		x[i], y[i] = xx, yy
	return x, y, rotation

