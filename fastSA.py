from bstree import Bstree

def cost_function(tree):
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
	net = 0
	for i in range(n_chiplet):
		for j in range(n_chiplet):
			if (i!=j) and (connection_matrix[i][j]>0):
				s.append(i)
				t.append(j)
				net += 1
	return net, s, t

def compute_wirelength(tree):
	total_wirelength = 0
	for i in range(net):
		s_index = tree.ind_arr.index(s[i])
		t_index = tree.ind_arr.index(t[i])
		wirelength = (abs(tree.x_arr[s_index] + tree.width_arr[s_index] / 2 - tree.x_arr[t_index] - tree.width_arr[t_index] / 2) + abs(tree.y_arr[s_index] + tree.height_arr[s_index] / 2 - tree.y_arr[t_index] - tree.height_arr[t_index] / 2)) * connection_matrix[s_index][t_index]
		total_wirelength += wirelength
	return total_wirelength

def anneal():
	# generate initial placement, and evaluate initial cost
	tree = Bstree()
	tree.flp2bstree(ind, x, y, width, height)
	tree.reconstruct()
	global net, s, t
	net, s, t = get_connections()
	cost = cost_function(tree)

	# set annealing parameters
	alpha = 0.85   # temperature decay factor


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

	anneal()

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
