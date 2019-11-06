class Node:
	def __init__(self, value = None, left = None, right = None):
		self.left = left
		self.right = right
		self.parent = None
		self.ind = value
		self.x = None
		self.y = None
		self.width = None
		self.height = None

	def set_node_value(self, value, x = None, y = None, width = None, height = None):
		self.ind = value
		self.x = x
		self.y = y
		self.width = width
		self.height = height

class Bstree:
	def __init__(self, root = None):
		self.root = root
		self.xpoint = set()
		self.ypoint = set()
		self.hct = []
		self.vct = []
		self.ind_arr = []
		self.x_arr = []
		self.y_arr = []
		self.width_arr = []
		self.height_arr = []

	def find_node(self, node, ind):
		if node == None:
			return None
		if node.ind == ind:
			return node
		res = self.find_node(node.left, ind)
		if res:
			return res
		return self.find_node(node.right, ind)

	def addnode(self, node, ind, x, y, width, height):
		# adding a new node (provided ind, x, y, width, height) to the left or right child of current node
		if node == None:
			return False
		if self.root.ind == None:
			self.root.set_node_value(ind, x, y, width, height)
			print ('Node ', ind, 'add to the root')
			return True
		elif x == node.x + node.width and y <= node.y + node.height and y + height >= node.y:
			if node.left == None:
				node.left = Node()
				node.left.set_node_value(ind, x, y, width, height)
				node.left.parent = node
				print ('Node ', ind, 'add to the left of ', node.ind)
				return True
		elif x == node.x:
			if node.right == None:
				node.right = Node()
				node.right.set_node_value(ind, x, y, width, height)
				node.right.parent = node
				print ('Node ', ind, 'add to the right of ', node.ind)
				return True
		# print (x, 'is not equal to either', node.x, 'or', node.x+node.width)
		try_right = self.addnode(node.right, ind, x, y, width, height)
		if not try_right:
			return self.addnode(node.left, ind, x, y, width, height)
		else:
			return True

	def flp2bstree(self, ox, oy, owidth, oheight):
		# x, y, width, height describes an admissible floorplan generated by a tight placement (or a naive side-by-side placement)
		# x, y are bottom-left coordinates of chiplet
		x, y, width, height = ox[:], oy[:], owidth[:], oheight[:]
		chiplet_count = len(x)
		ind = [i for i in range(chiplet_count)]
		x, y, width, height, ind = list(map(list, zip(*sorted(zip(x,y,width,height, ind), key=lambda pair: pair[0:2]))))
		print (ind, x, y, width, height)
		self.root = Node()
		# self.root.set_node_value(ind[0], x[0], y[0], width[0], height[0])
		print (self.root)
		for i in range(chiplet_count):
			self.addnode(self.root, ind[i], x[i], y[i], width[i], height[i])
		print ('print tree preorder')
		self.printTree(self.root)
		return self.root

	def resetloc(self, node):
		if node == None:
			return
		node.x, node.y = None, None
		self.resetloc(node.left)
		self.resetloc(node.right)

	def computex(self, node):
		if node == None:
			return
		self.xpoint.add(node.x)
		self.xpoint.add(node.x + node.width)
		if node.left:
			node.left.x = node.x + node.width
			self.computex(node.left)
		if node.right:
			node.right.x = node.x
			self.computex(node.right)

	def compacty(self, node):
		if node == None:
			return
		y = 0
		for i in range(len(self.xpoint)):
			if node.x <= self.xpoint[i] < node.x + node.width:
				y = max(y, self.hct[i])
		node.y = y
		for i in range(len(self.xpoint)):
			if node.x <= self.xpoint[i] < node.x + node.width:
				self.hct[i] = y + node.height
		self.ypoint.add(node.y)
		self.ypoint.add(node.y + node.height)
		self.compacty(node.left)
		self.compacty(node.right)

	def compactx(self, node):
		# reconstruct the bstree to make it admissible since rotate/move/swap may lead to non-compact structure.
		if node == None:
			return
		x = 0
		for i in range(len(self.ypoint)):
			if node.y <= self.ypoint[i] < node.y + node.height:
				x = max(x, self.vct[i])
		node.x = x
		for i in range(len(self.ypoint)):
			if node.y <= self.ypoint[i] < node.y + node.height:
				self.vct[i] = x + node.width
		self.compactx(node.left)
		self.compactx(node.right)

	def reconstruct(self):
		# need to recompute the x, y location. since the tree may have rotate/swap/move node
		self.resetloc(self.root)
		self.root.x = 0
		self.root.y = 0
		self.xpoint = set([0])
		self.computex(self.root)
		self.xpoint = sorted(list(self.xpoint))
		self.hct = [0] * len(self.xpoint) # hct for horizontal contour line
		print (self.xpoint)
		self.ypoint = set([0])
		self.compacty(self.root)
		self.ypoint = sorted(list(self.ypoint))
		self.vct = [0] * len(self.ypoint) # vct for vertical contour line
		print (self.ypoint)
		self.compactx(self.root)

	def rotate(self, node):
		# rotate do not change B*-tree structure, but will impact the flp
		node.width, node.height = node.height, node.width
		self.reconstruct()

	def swap(self, node1, node2):
		# instead of applying insert and delete operations, we use an alternative by swapping the index, width and height, but maintain the tree relationship and update the xy coordinates.
		node1.width, node2.width = node2.width, node1.width
		node1.height, node2.height = node2.height, node1.height
		node1.ind, node2.ind = node2.ind, node1.ind
		self.reconstruct()

	def delete(self, node):
		if node.left and node.right:
			# the node has two children
			snode = node
			while (snode.left and snode.right):
				self.swap(snode, snode.left)
				snode = snode.left
			if snode.left:
				snode.parent.left = snode.left
				snode.left.parent = snode.parent
			elif snode.right:
				snode.parent.left = snode.right
				snode.right.parent = snode.parent
			else:
				snode.parent.left = None
				snode.parent = None
		elif node.left:
			# the node has only left child
			if node.parent.left == node:
				node.parent.left = node.left
			elif node.parent.right == node:
				node.parent.right = node.left
			node.left.parent = node.parent
		elif node.right:
			# the node has only right child
			if node.parent.left == node:
				node.parent.left = node.right
			elif node.parent.right == node:
				node.parent.right = node.right
			node.right.parent = node.parent
		else:
			# the node is a leaf, just delete it
			if node.parent.left == node:
				node.parent.left = None
			elif node.parent.right == node:
				node.parent.right = None
			node.parent = None
		return node

	def insert(self, node, parent, direction):
		# add the node to the leaf of the parent, direction indicates left or right child
		if parent == None:
			# the only case the parent is none is to insert the node to the root
			if direction == 'left':
				node.left = self.root
				self.root.parent = node
				node.right = None
				node.parent = None
				self.root = node
			elif direction == 'right':
				node.right = self.root
				self.root.parent = node
				node.left = None
				node.parent = None
				self.root = node
		elif direction == 'left':
			if parent.left:
				node.left = parent.left
				parent.left.parent = node
				node.right = None
			parent.left = node
			node.parent = parent
		elif direction == 'right':
			if parent.right:
				node.right = parent.right
				parent.right.parent = node
				node.left = None
			parent.right = node
			node.parent = parent

	def move(self, node1, node2, direction):
		node = self.delete(node1)
		self.insert(node, node2, direction)



	def printTree(self, tree):
		if tree == self.root:
			print ('ind', 'x', 'y', 'width', 'height', 'parent','left','right', sep = '\t')
		if tree != None:
			print (tree.ind, tree.x, tree.y, tree.width, tree.height, tree.parent.ind if tree.parent else None, tree.left.ind if tree.left else None, tree.right.ind if tree.right else None, sep='\t')
			self.printTree(tree.left)
			self.printTree(tree.right)

if __name__ == "__main__":
	# example 1
	# x = [0, 2, 2, 0]
	# y = [0, 0, 1, 3]
	# width = [2, 1, 2, 3]
	# height = [2, 1, 2, 1]

	# example 2
	# node   0  1    2  3    4    5  6  7
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
	root = tree.flp2bstree(x, y, width, height)
	tree.resetloc(root)
	print (' ')
	tree.printTree(root)
	tree.reconstruct()
	print (' ')
	tree.printTree(root)
	# tree.swap(root.left, root.right)
	# tree.move(tree.find_node(root, 1), root.parent, 'left')
	del_node = tree.delete(tree.find_node(root, 1))
	tree.reconstruct()
	print (' ')
	tree.printTree(root)
	tree.insert(del_node, root.parent, 'left')
	tree.reconstruct()
	print (' ')
	tree.printTree(tree.root)
	print (tree.root.ind)

