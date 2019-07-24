import random
import numpy as np
import config
import block_occupation

def boundary_check(system, p, x, y):
	if (x - system.width[p] / 2) < 0:
		return False
	if (x + system.width[p] / 2) > system.intp_size:
		return False
	if (y - system.height[p] / 2) < 0:
		return False
	if (y + system.height[p] / 2) > system.intp_size:
		return False
	return True

def close_neighbor(system, grid):
	''' slightly moving chiplets'''
	chiplet_order = np.random.permutation(range(system.chiplet_count))
	granularity = system.granularity
	for p in chiplet_order:
		direction_order = np.random.permutation(['up', 'down', 'left', 'right'])
		xx, yy, width, height = system.x[p], system.y[p], system.width[p], system.height[p]
		# print ('chiplet ', p + 2)
		for d in direction_order:
			# print (d)
			if d == 'left':
				if block_occupation.check_down_occupation(grid, granularity, xx, yy - granularity, width, height):
					return p, xx, yy - granularity
			elif (d == 'right') and (yy + granularity <= system.intp_size):
				if block_occupation.check_up_occupation(grid, granularity, xx, yy + granularity, width, height):
					return p, xx, yy + granularity
			elif d == 'up':
				if block_occupation.check_left_occupation(grid, granularity, xx - granularity, yy, width, height):
					return p, xx - granularity, yy
			elif (d == 'down') and (xx + granularity <= system.intp_size):
				if block_occupation.check_right_occupation(grid, granularity, xx + granularity, yy, width, height):
					return p, xx + granularity, yy
	print ('No chiplet can be moved.')
	exit()

def random_neighbor(system, grid):
	'''define a neighbor placement as move one chiplet to anywhere can be located. 
	rotate if needed. We do not consider swapping, since can't gaurantee the placement
	is still legal (no overlap) after swapping'''

	n = system.chiplet_count
	granularity = system.granularity
	count = 0
	while True:
		pick_chiplet = random.randint(0, n - 1)
		x_new = random.randint(1, system.intp_size / granularity - 1) * granularity
		y_new = random.randint(1, system.intp_size / granularity - 1) * granularity
		if boundary_check(system, pick_chiplet, x_new, y_new) and block_occupation.replace_block_occupation(grid, granularity, system.x[pick_chiplet], system.y[pick_chiplet], x_new, y_new, system.width[pick_chiplet], system.height[pick_chiplet], pick_chiplet):
			break
		count += 1
		if count > 10000:
			# it's not easy to find a legal placement using random method. try move each chiplet (in random order) slightly until find a legal solution
			close_neighbor(system, grid)
			break
	return pick_chiplet, x_new, y_new

def anneal():
	# first step: read config and generate initial placement
	system = config.read_config()
	step = 0
	system.gen_flp('step_'+str(step))
	system.gen_ptrace('step_'+str(step))
	# temp_current = system.run_hotspot('step_'+str(step))
	# temp_best = temp_current
	# print ('step_'+str(step), temp_current)
	step_best = 0
	x_best, y_best = system.x[:], system.y[:]
	intp_size = system.intp_size
	granularity = system.granularity
	grid = block_occupation.initialize_grid(int(intp_size/granularity))
	for i in range(system.chiplet_count):
		grid = block_occupation.set_block_occupation(grid, granularity, system.x[i], system.y[i], system.width[i], system.height[i], i)

	print (close_neighbor(system, grid))

	# set annealing parameters
	T = 1.0
	T_min = 0.01
	alpha = 0.8
	# while T>T_min:
	# 	i = 1
	# 	while i <= intp_size:
	# 		step += 1
	# 		print ('step_'+str(step), ' T = ',T, ' i = ', i)

if __name__ == "__main__":
	anneal()
