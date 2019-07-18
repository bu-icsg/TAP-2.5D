import init_placement

class System_25D:
	# definiation of 2.5D system object, parent class, common properties and behaviors

	def __init__(self):
		self.chiplet_count = 0
		self.width = [None] * self.chiplet_count
		self.height = [None] * self.chiplet_count
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

	def initial_placement(self, init_place_option):
		if init_place_option == 'tight':
			x, y, rotation = init_placement.init_place_tight(self.intp_size, self.granularity, self.chiplet_count, self.width, self.height)
			self.x = x
			self.y = y
			self.rotation = rotation

	def gen_flp(self):
		pass