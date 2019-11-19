# for initial placement, I don't think it's very necessary to define a new class. 
# use a seperate module is clean enough

import random, math, os
import block_occupation
import fastSA

'''
I use occupation grid (the matrix) to present and check if the unit grid is available or
if it is already occupied. The grid (x, y) represent a unit square centered at (x,y) 
(area from [x-0.5, x+0.5] * [y-0.5, y+0.5])
'''

# width and height here include microbump overhead. We did addition before calling this module
def slide_x_direction(grid, granularity, xx, yy, width, height):
	while block_occupation.check_left_occupation(grid, granularity, xx-granularity, yy, width, height):
		xx -= granularity
	return xx

def slide_y_direction(grid, granularity, xx, yy, width, height):
	while block_occupation.check_down_occupation(grid, granularity, xx, yy-granularity, width, height):
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
	# block_occupation.print_grid(grid)
	return x, y, rotation

def init_place_bstree(intp_size, granularity, chiplet_count, width, height, connection_matrix):
	# step 1: construct initial bstree and run fast SA
	x, y = [0] * chiplet_count, [0] * chiplet_count
	ind = [i for i in range(chiplet_count)]
	tree, step_best, cost_best = fastSA.anneal(ind, x, y, width, height, connection_matrix)
	tree.printTree(tree.root)
	tree.gen_flp('best')
	print ('step_best = ', step_best)
	print ('wirelength = ', cost_best)
	os.system('gs -dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite -sOutputFile=outputs/bstree/comb_init.pdf outputs/bstree/step_{1..'+str(step_best)+'}sim.pdf')

	# step 2: relax the bstree structure, here the x, y coordinates are still left-bottom coordinates
	grid = block_occupation.initialize_grid(int(intp_size/granularity))
	tree.root.x = 0
	tree.root.y = 0
	tree.xpoint = set([0])
	tree.relax_x(tree.root, granularity)
	tree.xpoint = sorted(list(tree.xpoint))
	tree.bstree2flp()
	tree.hct = [0] * chiplet_count
	tree.ypoint = set([0])
	tree.relax_y(tree.root, granularity)
	tree.ypoint = sorted(list(tree.ypoint))
	tree.bstree2flp()
	tree.gen_flp('relax')
	tree.printTree(tree.root)

	# step 3: convert left-bottom coordinates to center coordinates.
	x_max, y_max = 0, 0
	for i in range(chiplet_count):
		tree.x_arr[i] = math.ceil((tree.x_arr[i] + 0.05 + tree.width_arr[i] / 2) / granularity) * granularity
		x_max = max(x_max, tree.x_arr[i] + tree.width_arr[i] / 2)
		tree.y_arr[i] = math.ceil((tree.y_arr[i] + 0.05 + tree.height_arr[i] / 2) / granularity) * granularity
		y_max = max(y_max, tree.y_arr[i] + tree.height_arr[i] / 2)
	print (tree.ind_arr, tree.x_arr, tree.y_arr, tree.width_arr, tree.height_arr, sep='\n')

	# step 4: move the chiplets to the center. offset all x and y's
	x_offset = int((intp_size - x_max) / 2 / granularity) * granularity
	y_offset = int((intp_size - y_max) / 2 / granularity) * granularity
	for i in range(chiplet_count):
		tree.x_arr[i] += x_offset
		tree.y_arr[i] += y_offset
	x, y, width, height = tree.x_arr[:], tree.y_arr[:], tree.width_arr[:], tree.height_arr[:]
	return x, y, width, height

if __name__ == "__main__":
	width = [3, 4, 	 2, 2, 	 1,   4, 3, 4]
	height =[2, 1.5, 3, 1.5, 1,   1, 2, 2]
	connection_matrix = [[0,128,128,0,0,0,0,128],
						[128,0,128,0,0,0,128,0],
						[128,128,0,128,128,128,128,128],
						[0,0,128,0,0,0,0,0],
						[0,0,128,0,0,0,0,0],
						[0,0,128,0,0,0,0,0],
						[0,128,128,0,0,0,0,128],
						[128,0,128,0,0,0,128,0]]
	x, y, rotation = init_place_bstree(40, 1, 8, width, height, connection_matrix)
