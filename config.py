import configparser
from system import System_25D

def get_intp_types():
	return ['passive']

def get_list(option):
	return list(map(float, ''.join(option.split()).split(',')))

def get_matrix(option):
	matrix = []
	for i in ''.join(option.split()).split(';'):
		matrix.append(list(map(int,i.split(','))))
	return matrix

def read_config():
	config = configparser.ConfigParser()
	config.read('example.cfg')

	path = config.get('general', 'path')

	try:
		granularity = config.getfloat('general', 'pddlacer_granularity')
	except:
		granularity = 1.0

	try:
		init_place_option = config.get('general', 'initial_placement')
	except:
		init_place_option = 'tight'

	interposer_type = config.get('interposer', 'intp_type')
	assert interposer_type in get_intp_types(), 'only support for passive interposer so far (to update with active, photonic, and EMIB options)'
	interposer_size = config.getfloat('interposer', 'intp_size')

	chiplet_count = config.getint('chiplets', 'chiplet_count')
	chiplet_width = get_list(config.get('chiplets', 'widths'))
	chiplet_height = get_list(config.get('chiplets', 'heights'))
	chiplet_power = get_list(config.get('chiplets', 'powers'))
	chiplet_connection = get_matrix(config.get('chiplets', 'connections'))

	system = System_25D(chiplet_count)
	return system

if __name__ == "__main__":
	system = read_config()
	print (system.chiplet_count, system.power)

