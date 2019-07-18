import config


if __name__ == "__main__":
	# read config file and initialize the parameters
	system = config.read_config()
	print (system.chiplet_count, system.intp_size, system.power, system.x)
	
	system.gen_flp('test')