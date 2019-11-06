from bstree import Bstree

def cost_function(A, W):
	return 0.1 * A + 0.9 * W

def accept_probability(old_cost, new_cost, T):
	delta = - (new_cost - old_cost)
	if delta > 0:
		ap = 1
	else:
		ap = math.exp(delta / T )
	return ap

def anneal():
	alpha = 0.85   # temperature decay factor


if __name__ == "__main__":
	# example 1
	# x = [0, 2, 2, 0]
	# y = [0, 0, 1, 3]
	# width = [2, 1, 2, 3]
	# height = [2, 1, 2, 1]

	# example 2
	# node   0  1    2  3    4    5  6  7
	ind = 	[0, 1,   2, 3, 	 4,   5, 6, 7]
	x = 	[0, 3, 	 0, 3, 	 5,   2, 0, 3]
	y = 	[0, 0, 	 2, 1.5, 1.5, 3, 5, 4]
	width = [3, 4, 	 2, 2, 	 1,   4, 3, 4]
	height =[2, 1.5, 3, 1.5, 1,   1, 2, 2]

	# example 3
	# x = [0, 0, 1, 1]
	# y = [0, 1, 0, 1]
	# width = [1,1,1,1]
	# height = [1,1,1,1]
	
	tree = Bstree()
	root = tree.flp2bstree(ind, x, y, width, height)
	# tree.swap(root.left, root.right)
	# tree.move(tree.find_node(root, 1), root.parent, 'left')
	del_node = tree.delete(tree.find_node(tree.root, 1))
	tree.reconstruct()
	print ('after delete node 1')
	tree.printTree(tree.root)
	tree.insert(del_node, tree.root.parent, 'left')
	tree.reconstruct()
	print ('\n after insert node 1 to the root')
	tree.printTree(tree.root)
	print (tree.root.ind)

	tree.bstree2flp()
