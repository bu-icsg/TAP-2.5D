from bstree import Bstree
from copy import deepcopy
import random, math, os

def cost_function(tree, cost_norm):
	W = compute_wirelength(tree)
	return W

def accept_probability(old_cost, new_cost, T):
	delta = - (new_cost - old_cost)
	if delta > 0:
		ap = 1
	else:
		ap = math.exp(delta / T )
	return ap

def get_connections():
	s, t = [], []
	net, wire_count = 0, 0
	for i in range(n_chiplet):
		for j in range(n_chiplet):
			if (i!=j) and (connection_matrix[i][j]>0):
				s.append(i)
				t.append(j)
				net += 1
				wire_count += connection_matrix[i][j]
	return net, s, t, wire_count

def compute_wirelength(tree):
	total_wirelength = 0
	for i in range(net):
		s_index = tree.ind_arr.index(s[i])
		t_index = tree.ind_arr.index(t[i])
		# print (tree.ind_arr, tree.x_arr, tree.y_arr, tree.width_arr, tree.height_arr, sep='\n')
		# print (len(tree.ind_arr), s_index, t_index)
		wirelength = (abs(tree.x_arr[s_index] + tree.width_arr[s_index] / 2 - tree.x_arr[t_index] - tree.width_arr[t_index] / 2) + abs(tree.y_arr[s_index] + tree.height_arr[s_index] / 2 - tree.y_arr[t_index] - tree.height_arr[t_index] / 2)) * connection_matrix[s_index][t_index]
		total_wirelength += wirelength
	return total_wirelength / wire_count

def neighbor(tree):
	tree_new = deepcopy(tree)
	op_dice = random.randint(0, n_chiplet + 2 * n_chiplet * n_chiplet + n_chiplet *(n_chiplet-1)/2 - 1)
	if op_dice < n_chiplet:
		# rotate, only determine which node to rotate
		print ('rotate node', op_dice)
		tree_new.rotate(tree_new.find_node(tree_new.root, tree_new.ind_arr[op_dice]))
	elif n_chiplet <= op_dice < n_chiplet + n_chiplet * (n_chiplet - 1) / 2:
		# swap, determine two nodes
		n1 = random.randint(0, n_chiplet - 1)
		n2 = random.randint(0, n_chiplet - 1)
		while n2 == n1:
			n2 = random.randint(0, n_chiplet - 1)
		node1 = tree_new.find_node(tree_new.root, tree_new.ind_arr[n1])
		node2 = tree_new.find_node(tree_new.root, tree_new.ind_arr[n2])
		print ('swap nodes', n1, 'and', n2)
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
			print ('move node', n1, 'to the root')
		else:
			print ('move node', n1, 'to the', dirs, 'child of node', n2)
		tree_new.move(node1, node2, dirs)
	tree_new.reconstruct()
	return tree_new

def anneal():
	# generate initial placement, and evaluate initial cost
	tree = Bstree()
	tree.flp2bstree(ind, x, y, width, height)
	tree.reconstruct()
	tree_best = deepcopy(tree)
	global net, s, t, wire_count
	net, s, t, wire_count = get_connections()
	cost_norm = 1
	cost_current = cost_function(tree, cost_norm)
	cost_best = cost_current
	step, step_best = 1, 1

	# set annealing parameters
	# alpha = 0.99   	# temperature decay factor
	T = 8			# check the paper
	T_min = 0.01	# check the paper
	c = 100
	k = 7

	print ('initial tree')
	tree.printTree(tree.root)
	tree.gen_flp('step_1')

	while step <= k or T > T_min:
		step += 1
		print ('step_'+str(step), ' T=', T)
		tree_new = neighbor(tree)
		tree_new.printTree(tree_new.root)
		tree_new.gen_flp('step_'+str(step))
		cost_new = cost_function(tree_new, cost_norm)
		print ('wirelength = ', cost_new)
		ap = accept_probability(cost_current, cost_new, T)
		r = random.random()
		if ap > r:
			tree = deepcopy(tree_new)
			cost_current = cost_new
			if cost_current < cost_best:
				cost_best = cost_current
				tree_best = deepcopy(tree)
				step_best = step
			print ('AP = ', ap, ' > ', r, ' Accept!')
		else:
			print ('AP = ', ap, ' < ', r, ' Reject!')
		# T *= alpha
		if step <= k:
			T = 0.067/step
		else:
			T = 6.7/step
	return tree_best, step_best, cost_best

if __name__ == "__main__":
	# initial placement
	# node   0  1    2  3    4    5  6  7
	ind = 	[0, 1,   2, 3, 	 4,   5, 6, 7]
	x = 	[0, 3, 	 0, 3, 	 5,   2, 0, 3]
	y = 	[0, 0, 	 2, 1.5, 1.5, 3, 5, 4]
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
	n_chiplet = len(connection_matrix)

	tree_best, step_best, cost_best = anneal()
	tree_best.printTree(tree_best.root)
	tree_best.gen_flp('best')
	print ('step_best = ', step_best)
	print ('wirelength = ', cost_best)
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
