class System_passive:
	# definiation of 2.5D system object with passive silicon interposer
	def __init__(self, size):
		self.intp_size = size
		self.chiplet_count = 0
		self.chiplets = []
