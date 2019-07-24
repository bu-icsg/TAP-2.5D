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

def check_left_occupation(grid, granularity, xx, yy, width, height):
	i = int(xx/granularity) - int(width/2/granularity+0.49)
	if i<=0:
		return False
	if (sum(grid[i][int(yy/granularity)-int(height/2/granularity+0.49):int(yy/granularity)+int(height/2/granularity+0.49)+1])):
		# print (i, grid[i][int(yy/granularity)-int(height/2/granularity+0.49):int(yy/granularity)+int(height/2/granularity+0.49)+1])
		return False
	else:
		return True

def check_right_occupation(grid, granularity, xx, yy, width, height):
	i = int(xx/granularity) + int(width/2/granularity+0.49)
	intp_size = (len(grid) - 1) * granularity
	if i >= intp_size:
		return False
	if (sum(grid[i][int(yy/granularity)-int(height/2/granularity+0.49):int(yy/granularity)+int(height/2/granularity+0.49)+1])):
		# print (i, grid[i][int(yy/granularity)-int(height/2/granularity+0.49):int(yy/granularity)+int(height/2/granularity+0.49)+1])
		return False
	else:
		return True

def check_down_occupation(grid, granularity, xx, yy, width, height):
	j = int(yy/granularity) - int(height/2/granularity+0.49)
	if j<=0:
		return False
	for i in range(int(xx/granularity)-int(width/2/granularity+0.49), int(xx/granularity)+int(width/2/granularity+0.49)+1):
		if grid[i][j]:
			# print (i,j, grid[i][j])
			return False
	return True

def check_up_occupation(grid, granularity, xx, yy, width, height):
	j = int(yy/granularity) + int(height/2/granularity+0.49)
	intp_size = (len(grid) - 1) * granularity
	if j >= intp_size:
		return False
	for i in range(int(xx/granularity)-int(width/2/granularity+0.49), int(xx/granularity)+int(width/2/granularity+0.49)+1):
		if grid[i][j]:
			# print (i,j, grid[i][j])
			return False
	return True

def set_block_occupation(grid, granularity, xx, yy, width, height, chiplet_index):
	for i in range(int(xx/granularity)-int(width/2/granularity+0.49), int(xx/granularity)+int(width/2/granularity+0.49)+1):
		for j in range(int(yy/granularity)-int(height/2/granularity+0.49), int(yy/granularity)+int(height/2/granularity+0.49)+1):
			grid[i][j] = chiplet_index + 2
	return grid

def clear_block_occupation(grid, granularity, xx, yy, width, height, chiplet_index):
	for i in range(int(xx/granularity)-int(width/2/granularity+0.49), int(xx/granularity)+int(width/2/granularity+0.49)+1):
		for j in range(int(yy/granularity)-int(height/2/granularity+0.49), int(yy/granularity)+int(height/2/granularity+0.49)+1):
			if grid[i][j] != chiplet_index + 2:
				print ("something wrong, chiplet index mismatch")
				exit()
			grid[i][j] = 0
	return grid

def replace_block_occupation(grid, granularity, xx, yy, xx_new, yy_new, width, height, chiplet_index):
	for i in range(int(xx/granularity)-int(width/2/granularity+0.49), int(xx/granularity)+int(width/2/granularity+0.49)+1):
		for j in range(int(yy/granularity)-int(height/2/granularity+0.49), int(yy/granularity)+int(height/2/granularity+0.49)+1):
			if (grid[i][j] != chiplet_index + 2) or (grid[i][j] != 0):
				return False
	return True