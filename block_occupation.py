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

