import configparser
from chiplet import Chiplet
from system import *

def read_config():
	config = configparser.ConfigParser()
	config.read('example.cfg')

	path = config.get('taco', 'path')
	interposer_type = config.get('taco', 'intp_type')
	assert interposer_type in ['passive'], 'only support for passive interposer so far (to update with active, photonic, and EMIB options)'
	interposer_size = config.getfloat('taco', 'intp_size')
	if interposer_type == 'passive':
		system = System_passive(interposer_size)

	n_chiplet_type = config.getint('2.5D', 'n_chiplet_type')
	n_chiplet, width_config, height_config, power_config = [0] * n_chiplet_type, [0] * n_chiplet_type, [0] * n_chiplet_type, [0] * n_chiplet_type
	n_chiplet_total = 0

	'''read from the simplified config file description'''
	for i in range(n_chiplet_type):
		n_chiplet[i] = config.getint('2.5D', 'n_chiplet_'+str(i))
		n_chiplet_total += n_chiplet[i]
		width_config[i] = config.getfloat('2.5D', 'width_'+str(i))
		height_config[i] = config.getfloat('2.5D', 'height_'+str(i))
		power_config[i] = config.getfloat('2.5D', 'power_'+str(i))
	system.chiplet_count = n_chiplet_total

	'''convert to standard description '''
	for i in range(n_chiplet_type):
		for j in range(n_chiplet[i]):
			system.chiplets.append(Chiplet(width_config[i], height_config[i], power_config[i]))

	return system

if __name__ == "__main__":
	system = read_config()
	for i in range(system.chiplet_count):
		print ('Chiplet', i, system.chiplets[i].width, system.chiplets[i].height, system.chiplets[i].power)


