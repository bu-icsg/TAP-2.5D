import config

def anneal():
	# first step: read config and generate initial placement
	system = config.read_config()
	system.gen_flp('test')
	system.gen_ptrace('test')
	temp = system.run_hotspot('test')

if __name__ == "__main__":
	anneal()