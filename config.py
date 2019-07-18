import configparser
import os
from passive_interposer import PassiveInterposer

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
		granularity = config.getfloat('general', 'placer_granularity')
	except:
		granularity = 1.0

	try:
		init_place_option = config.get('general', 'initial_placement')
	except:
		init_place_option = 'tight'

	interposer_type = config.get('interposer', 'intp_type')
	assert interposer_type in get_intp_types(), 'only support for passive interposer so far (to update with active, photonic, and EMIB options)'

	chiplet_count = config.getint('chiplets', 'chiplet_count')
	chiplet_width = get_list(config.get('chiplets', 'widths'))
	chiplet_height = get_list(config.get('chiplets', 'heights'))
	chiplet_power = get_list(config.get('chiplets', 'powers'))
	chiplet_connection = get_matrix(config.get('chiplets', 'connections'))

	if interposer_type == 'passive':
		interposer_size = config.getfloat('interposer', 'intp_size')
		system = PassiveInterposer()
		system.set_path(path)
		if os.path.exists(path) == False:
			os.system('mkdir -p ' + path)
		system.set_chiplet_count(chiplet_count)
		system.initialize()
		system.set_interposer_size(interposer_size)
		system.set_chiplet_power(chiplet_power)
		system.set_chiplet_size(chiplet_width, chiplet_height)
		system.set_connection_matrix(chiplet_connection)
		system.set_granularity(granularity)
		system.initial_placement(init_place_option)
	return system

if __name__ == "__main__":
	system = read_config()
	print (system.chiplet_count, system.intp_size, system.power, system.x)

