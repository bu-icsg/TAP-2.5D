import random, os, math
import numpy as np
import config
import block_occupation
from copy import deepcopy

def boundary_check(system, x, y, w, h):
	if (x - w / 2) < 0:
		return False
	if (x + w / 2) > system.intp_size:
		return False
	if (y - h / 2) < 0:
		return False
	if (y + h / 2) > system.intp_size:
		return False
	return True

def close_neighbor(system, grid):
	''' slightly moving chiplets, do not consider rotation'''
	chiplet_order = np.random.permutation(range(system.chiplet_count))
	granularity = system.granularity
	for p in chiplet_order:
		direction_order = np.random.permutation(['up', 'down', 'left', 'right'])
		xx, yy, width, height = system.x[p], system.y[p], system.width[p], system.height[p]
		# print ('chiplet ', p + 2)
		for d in direction_order:
			# print (d)
			# re-connect the direction with the appropriate function in order to easily visulize using print-grid(). The dirctions are referring to the grid printed on screen, the directions in functions are referring to conventional x-y coordinates, origin in the left-bottom corner.
			if d == 'left':
				if block_occupation.check_down_occupation(grid, granularity, xx, yy - granularity, width, height):
					print ('chiplet', p + 2, d)
					return p, xx, yy - granularity
			elif (d == 'right') and (yy + granularity <= system.intp_size):
				if block_occupation.check_up_occupation(grid, granularity, xx, yy + granularity, width, height):
					print ('chiplet', p + 2, d)
					return p, xx, yy + granularity
			elif d == 'up':
				if block_occupation.check_left_occupation(grid, granularity, xx - granularity, yy, width, height):
					print ('chiplet', p + 2, d)
					return p, xx - granularity, yy
			elif (d == 'down') and (xx + granularity <= system.intp_size):
				if block_occupation.check_right_occupation(grid, granularity, xx + granularity, yy, width, height):
					print ('chiplet', p + 2, d)
					return p, xx + granularity, yy
	print ('No chiplet can be moved.')
	exit()

def jumping_neighbor(system, grid):
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
		rotation = random.randint(0,1)
		if rotation == 1:
			chiplet_width, chiplet_height = system.height[pick_chiplet], system.width[pick_chiplet]
		else:
			chiplet_height, chiplet_width = system.height[pick_chiplet], system.width[pick_chiplet]
		if boundary_check(system, x_new, y_new, chiplet_width, chiplet_height) and block_occupation.replace_block_occupation(grid, granularity, x_new, y_new, chiplet_width, chiplet_height, pick_chiplet):
			print ('found a random placement at', count, 'th trial')
			break
		count += 1
		if count > 10000:
			# it's not easy to find a legal placement using random method. try move each chiplet (in random order) slightly until find a legal solution
			print ('cannot find a legal random placement, go with close_neighbor')
			return close_neighbor(system, grid)
	return pick_chiplet, x_new, y_new, rotation

# def accept_probability(old_temp, new_temp, old_length, new_length, T):
# 	if new_length <= length_threshold and old_length <= length_threshold:
# 		# already meet length threshold, highlight temperature term
# 		delta = 0.9 * (old_temp - new_temp) * 4.0 + 0.1 * (old_length - new_length)
# 	else:
# 		# not meet length threshold, highlight length term
# 		delta = 0.1 * (old_temp - new_temp) * 4.0 + 0.9 * (old_length - new_length)
# 	# delta = (old_temp - new_temp) * 4.0 + min(0, length_threshold - new_length)
# 	print old_temp, new_temp, old_length, new_length, T, delta
# 	if delta > 0:
# 		ap = 1
# 	else:
# 		ap = math.exp( delta / T )
# 	return ap

def accept_probability(old_temp, new_temp, T):
	delta = (old_temp - new_temp)
	# delta = (old_temp - new_temp) * 4.0 + min(0, length_threshold - new_length)
	# print (old_temp, new_temp, T, delta)
	if delta > 0:
		ap = 1
	else:
		ap = math.exp( delta / T )
	return ap

def anneal():
	# first step: read config and generate initial placement
	system = config.read_config()
	system_new = deepcopy(system)
	system_best = deepcopy(system)
	step = 0
	system.gen_flp('step_'+str(step))
	system.gen_ptrace('step_'+str(step))
	temp_current = system.run_hotspot('step_'+str(step))
	temp_best = temp_current
	print ('step_'+str(step), temp_current)
	step_best = 0
	x_best, y_best = system.x[:], system.y[:]
	intp_size = system.intp_size
	granularity = system.granularity
	grid = block_occupation.initialize_grid(int(intp_size/granularity))
	for i in range(system.chiplet_count):
		grid = block_occupation.set_block_occupation(grid, granularity, system.x[i], system.y[i], system.width[i], system.height[i], i)
	block_occupation.print_grid(grid)
	# set annealing parameters
	T = 1.0
	T_min = 0.01
	alpha = 0.8
	jumping_ratio = T_min / alpha
	# start simulated annealing
	while T > T_min:
		i = 1
		while i <= intp_size:
			step += 1
			print ('step_'+str(step), ' T = ',T, ' i = ', i)
			jump_or_close = random.random()
			if 1 - jumping_ratio > jump_or_close:
				chiplet_moving, x_new, y_new, rotation = jumping_neighbor(system, grid)
			else:
				chiplet_moving, x_new, y_new = close_neighbor(system, grid)
				rotation = 0
			print ('moving chiplet', chiplet_moving + 2, 'from (', system.x[chiplet_moving], system.y[chiplet_moving], ') to (', x_new, y_new, '), rotation = ', rotation)
			system_new = deepcopy(system)
			system_new.x[chiplet_moving], system_new.y[chiplet_moving] = x_new, y_new
			if rotation == 1:
				system_new.rotate(chiplet_moving)
				# system_new.height[chiplet_moving], system_new.width[chiplet_moving] = system_new.width[chiplet_moving], system_new.height[chiplet_moving]
			system_new.gen_flp('step_' + str(step))
			system_new.gen_ptrace('step_'+str(step))
			temp_new = system_new.run_hotspot('step_'+str(step))
			print ('Temp = ', temp_new)
			ap = accept_probability(temp_current, temp_new, T)
			r = random.random()
			if ap > r:
				# clear last step's occupation of chiplet_moving (system)
				grid = block_occupation.clear_block_occupation(grid, granularity, system.x[chiplet_moving], system.y[chiplet_moving], system.width[chiplet_moving], system.height[chiplet_moving], chiplet_moving)
				# set new occupation with rotation (system_new)
				grid = block_occupation.set_block_occupation(grid, granularity, x_new, y_new, system_new.width[chiplet_moving], system_new.height[chiplet_moving], chiplet_moving)
				# update system
				system = deepcopy(system_new)
				temp_current = temp_new
				if temp_new < temp_best:
					temp_best = temp_new
					system_best = deepcopy(system_new)
					step_best = step
				print ('AP = ', ap, ' > ', r, ' Accept!')				
				block_occupation.print_grid(grid)
			else:
				print ('AP = ', ap, ' < ', r, ' Reject!')	
			i += 1
		T *= alpha
		jumping_ratio /= alpha
	os.system('rm '+ system.path + '{*.flp,*.lcf,*.ptrace,*.steady}')
	return system_best, step_best, temp_best

if __name__ == "__main__":
	solution, step_best, temp_best = anneal()
	print ('final solution: step, temp')
	print (step_best)
	print (temp_best)

