import config


if __name__ == "__main__":
	# read config file and initialize the parameters
	system = config.read_config()
	system.gen_flp('test')
	system.gen_ptrace('test')
	print (system.run_hotspot('test'))