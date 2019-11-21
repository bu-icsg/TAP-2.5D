from bstree import Bstree
from copy import deepcopy
import random, math, os

def accept_probability(wl_current, wl_new, area_current, area_new, T, step):
	# assume the weights for wirelength and area term are equal
	if wl_min != wl_max and area_min != area_max:
		old_cost = 0.5 * (wl_current - wl_min) / (wl_max - wl_min) + 0.5 * (area_current - area_min) / (area_max - area_min)
		new_cost = 0.5 * (wl_new - wl_min) / (wl_max - wl_min) + 0.5 * (area_new - area_min) / (area_max - area_min)
	else:
		old_cost = 0.5 * (wl_current - wl_min) + 0.5 * (area_current - area_min)
		new_cost = 0.5 * (wl_new - wl_min) + 0.5 * (area_new - area_min)
	global cost_chg_avg
	cost_chg_avg = (cost_chg_avg * (step-1) + abs(new_cost - old_cost)) / step
	delta = - (new_cost - old_cost)
	if delta > 0:
		ap = 1
	else:
		ap = math.exp(delta / T )
	return ap

def get_connections(connection_matrix):
	# get connection information. One time execution
	s, t = [], []
	net, wire_count = 0, 0
	n_chiplet = len(connection_matrix)
	for i in range(n_chiplet):
		for j in range(n_chiplet):
			if (i!=j) and (connection_matrix[i][j]>0):
				s.append(i)
				t.append(j)
				net += 1
				wire_count += connection_matrix[i][j]
	return net, s, t, wire_count

def compute_wirelength(tree, step, connection_matrix):
	# length_per_wire value, do not normalize
	total_wirelength = 0
	for i in range(net):
		s_index = tree.ind_arr.index(s[i])
		t_index = tree.ind_arr.index(t[i])
		# print (tree.ind_arr, tree.x_arr, tree.y_arr, tree.width_arr, tree.height_arr, sep='\n')
		# print (len(tree.ind_arr), s_index, t_index)
		wirelength = (abs(tree.x_arr[s_index] + tree.width_arr[s_index] / 2 - tree.x_arr[t_index] - tree.width_arr[t_index] / 2) + abs(tree.y_arr[s_index] + tree.height_arr[s_index] / 2 - tree.y_arr[t_index] - tree.height_arr[t_index] / 2)) * connection_matrix[s_index][t_index]
		total_wirelength += wirelength
	wl = total_wirelength / wire_count
	# update the wirelength stats for normalization
	global wl_max, wl_min
	if wl > wl_max:
		wl_max = wl
	if wl < wl_min:
		wl_min = wl
	return wl

def compute_area(tree, step):
	n_chiplet = len(tree.ind_arr)
	edge = 0
	for i in range(n_chiplet):
		if edge < tree.x_arr[i] + tree.width_arr[i]:
			edge = tree.x_arr[i] + tree.width_arr[i]
		if edge < tree.y_arr[i] + tree.height_arr[i]:
			edge = tree.y_arr[i] + tree.height_arr[i]
	global area_max, area_min
	if edge > area_max:
		area_max = edge
	if edge < area_min:
		area_min = edge
	return edge

def neighbor(tree):
	tree_new = deepcopy(tree)
	n_chiplet = len(tree.ind_arr)
	op_dice = random.randint(0, n_chiplet + 2 * n_chiplet * n_chiplet + n_chiplet *(n_chiplet-1)/2 - 1)
	if op_dice < n_chiplet:
		# rotate, only determine which node to rotate
		try:
			DEBUG
			print ('rotate node', op_dice)
		except NameError:
			pass
		tree_new.rotate(tree_new.find_node(tree_new.root, tree_new.ind_arr[op_dice]))
	elif n_chiplet <= op_dice < n_chiplet + n_chiplet * (n_chiplet - 1) / 2:
		# swap, determine two nodes
		n1 = random.randint(0, n_chiplet - 1)
		n2 = random.randint(0, n_chiplet - 1)
		while n2 == n1:
			n2 = random.randint(0, n_chiplet - 1)
		node1 = tree_new.find_node(tree_new.root, tree_new.ind_arr[n1])
		node2 = tree_new.find_node(tree_new.root, tree_new.ind_arr[n2])
		try:
			DEBUG
			print ('swap nodes', n1, 'and', n2)
		except NameError:
			pass
		tree_new.swap(node1, node2)
	else:
		# move, determine the node to move, and the target position (left/right child of other nodes or insert to replace root)
		n1 = random.randint(0, n_chiplet - 1)
		n2 = random.randint(0, n_chiplet - 1)
		d = random.randint(0, 1)
		dirs = 'right' if d else 'left'
		node1 = tree_new.find_node(tree_new.root, tree_new.ind_arr[n1]) # the node to be moved
		node2 = tree_new.find_node(tree_new.root, tree_new.ind_arr[n2]) # the parent node that the moved node is going to insert to.
		if n1 == n2:
			if tree_new.root == node2:
				return neighbor(tree)
			node2 = tree_new.root.parent
			try:
				DEBUG
				print ('move node', n1, 'to the root')
			except NameError:
				pass
		else:
			try:
				DEBUG
				print ('move node', n1, 'to the', dirs, 'child of node', n2)
			except NameError:
				pass
		tree_new.move(node1, node2, dirs)
	tree_new.reconstruct()
	return tree_new

def anneal(ind, x, y, width, height, connection_matrix):
	# generate initial placement, and evaluate initial cost
	step, step_best = 1, 1
	tree = Bstree()
	tree.flp2bstree(ind, x, y, width, height)
	tree.reconstruct()
	tree_best = deepcopy(tree)
	global net, s, t, wire_count
	net, s, t, wire_count = get_connections(connection_matrix)
	global wl_max, wl_min, cost_chg_avg
	global area_max, area_min   # we use the longer edge length to represent interposer area
	wl_max, wl_min= 0, 100
	area_max, area_min = 0, 100
	cost_chg_avg = 0
	wl_current = compute_wirelength(tree, step, connection_matrix)
	wl_best = wl_current
	area_current = compute_area(tree, step)
	area_best = area_current
	reject_cont = 0

	# set annealing parameters
	# alpha = 0.99   	# temperature decay factor
	T1 = 10			# check the paper
	T = T1
	# T_min = 0.01	# check the paper
	# instead of T_min, use 100 consecutive reject as stopping condition
	c = 100
	k = 7

	try:
		DEBUG
		print ('initial tree')
		tree.printTree(tree.root)
		tree.gen_flp('step_1')
	except NameError:
		pass

	while step < 1000:
		step += 1
		tree_new = neighbor(tree)
		# tree_new.printTree(tree_new.root)
		tree_new.gen_flp('step_'+str(step))
		wl_new = compute_wirelength(tree_new, step, connection_matrix)
		area_new = compute_area(tree_new, step)
		try:
			DEBUG
			print ('step_'+str(step), ' T=', T, ' avg_change =', cost_chg_avg, ' reject=', reject_cont, ' best=', wl_best)
			print ('wirelength = ', wl_new, 'area = ', area_new)
		except NameError:
			pass
		ap = accept_probability(wl_current, wl_new, area_current, area_new, T, step)
		r = random.random()
		if ap > r:
			tree = deepcopy(tree_new)
			wl_current = wl_new
			area_current = area_new
			if wl_current < wl_best:
				wl_best = wl_current
				area_best = area_current
				tree_best = deepcopy(tree)
				step_best = step
			try:
				DEBUG
				print ('AP = ', ap, ' > ', r, ' Accept!')
			except NameError:
				pass
			reject_cont = 0
		else:
			try:
				DEBUG
				print ('AP = ', ap, ' < ', r, ' Reject!')
			except NameError:
				pass			
			reject_cont += 1
			if reject_cont > 35:
				try:
					DEBUG
					print ('hit early stop condition')
				except NameError:
					pass
				break
		# T *= alpha
		if step <= k:
			T = T1 * (cost_chg_avg + 0.000001) / 100 / step
		else:
			T = T1 * (cost_chg_avg + 0.000001) / step
	print ('wirelength_best = ', wl_best, 'area_best', area_best)
	return tree_best, step_best, wl_best

if __name__ == "__main__":
	DEBUG = True
	# initial placement
	# node   0  1    2  3    4    5  6  7
	ind = 	[0, 1,   2, 3, 	 4,   5, 6, 7]
	x = 	[0, 3, 	 0, 3, 	 5,   2, 0, 3]
	y = 	[0, 0, 	 2, 1.5, 1.5, 3, 5, 4]
	width = [3, 4, 	 2, 2, 	 1,   4, 3, 4]
	height =[2, 1.5, 3, 1.5, 1,   1, 2, 2]

	# example 2
	ind = 	[0,   1,   2,   3,   4, 5, 6, 7]
	x = 	[0,   0,   0,   0,   0, 0, 0, 0]
	y = 	[0,   0,   0,   0,   0, 0, 0, 0]
	width = [3,   4,   2,   2,   1, 4, 3, 4]
	height =[2,   1.5, 3,   1.5, 1, 1, 2, 2]

	connection_matrix = [[0,128,128,0,0,0,0,128],
						[128,0,128,0,0,0,128,0],
						[128,128,0,128,128,128,128,128],
						[0,0,128,0,0,0,0,0],
						[0,0,128,0,0,0,0,0],
						[0,0,128,0,0,0,0,0],
						[0,128,128,0,0,0,0,128],
						[128,0,128,0,0,0,128,0]]
	n_chiplet = len(connection_matrix)

	tree_best, step_best, wl_best = anneal(ind, x, y, width, height, connection_matrix)
	tree_best.printTree(tree_best.root)
	tree_best.gen_flp('best')
	print ('step_best = ', step_best)
	print ('wirelength = ', wl_best)
	os.system('gs -dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite -sOutputFile=outputs/bstree/combine.pdf outputs/bstree/step_{1..'+str(step_best)+'}sim.pdf')

	# tree = Bstree()
	# root = tree.flp2bstree(ind, x, y, width, height)
	# # tree.swap(root.left, root.right)
	# # tree.move(tree.find_node(root, 1), root.parent, 'left')
	# del_node = tree.delete(tree.find_node(tree.root, 1))
	# tree.reconstruct()
	# print ('after delete node 1')
	# tree.printTree(tree.root)
	# tree.insert(del_node, tree.root.parent, 'left')
	# tree.reconstruct()
	# print ('\n after insert node 1 to the root')
	# tree.printTree(tree.root)
	# print (tree.root.ind)
	# tree.bstree2flp()
