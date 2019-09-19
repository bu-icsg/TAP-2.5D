import init_placement

class System_25D:
	# definiation of 2.5D system object, parent class, common properties and behaviors

	def __init__(self):
		self.chiplet_count = 0
		self.width = [None] * self.chiplet_count
		self.height = [None] * self.chiplet_count
		self.hubump = [None] * self.chiplet_count
		self.power = [None] * self.chiplet_count
		self.rotation = [None] * self.chiplet_count
		self.x = [None] * self.chiplet_count
		self.y = [None] * self.chiplet_count

	def set_path(self, path):
		self.path = path

	def set_interposer_size(self, intp_size):
		self.intp_size = intp_size

	def set_chiplet_count(self, chiplet_count):
		self.chiplet_count = chiplet_count

	def initialize(self):
		self.rotation = [0] * self.chiplet_count
		self.width = [None] * self.chiplet_count
		self.height = [None] * self.chiplet_count
		self.hubump = [None] * self.chiplet_count
		self.power = [None] * self.chiplet_count
		self.x = [None] * self.chiplet_count
		self.y = [None] * self.chiplet_count
		self.ubump = 0

	def set_chiplet_size(self, width, height):
		self.width = width
		self.height = height

	def set_chiplet_power(self, power):
		self.power = power

	def set_connection_matrix(self, connection):
		self.connection_matrix = connection

	def set_granularity(self, granularity):
		self.granularity = granularity

	def rotate(self, i):
		self.width[i], self.height[i] = self.height[i], self.width[i]

	def initial_placement(self, init_place_option, xx, yy):
		new_width, new_height = [None] * self.chiplet_count, [None] * self.chiplet_count
		for i in range(self.chiplet_count):
			new_width[i] = self.width[i] + 2 * self.hubump[i]
			new_height[i] = self.height[i] + 2 * self.hubump[i]
		if init_place_option == 'tight':
			x, y, rotation = init_placement.init_place_tight(self.intp_size, self.granularity, self.chiplet_count, new_width, new_height)
			self.x = x
			self.y = y
			self.rotation = rotation
		elif init_place_option == 'given':
			self.x = xx
			self.y = yy

	def gen_flp(self):
		pass

	def gen_ptrace(self):
		pass

	def run_hotspot(self):
		pass

	def compute_ubump_overhead(self):
		connection = self.connection_matrix
		for i in range(self.chiplet_count):
			assert connection[i][i] == 0, 'a link from and to the same chiplet is not allowed'
			s = 0
			for j in range(self.chiplet_count):
				s += connection[i][j] + connection[j][i]
			h = 1
			w_stretch = 0.045 * h
			while ((self.width[i] + self.height[i]) * 2 * w_stretch + 4 * w_stretch * w_stretch) / 0.045 / 0.045 < s:
				h += 1
				w_stretch = 0.045 * h
				if h > 1000:
					print ('microbump is too high to be a feasible case')
					exit()
			# print (i, s, self.width[i], self.height[i], h, w_stretch)
			self.hubump[i] = w_stretch
		print (self.hubump)

