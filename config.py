import configparser
import getopt
import os, sys
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
	opts = parse_command()

	# default config filename
	filename = 'example.cfg'
	path = None
	overwrite = []
	interposer_size = 0
	for o, a in opts:
		if o == '-h':
			usage()
			sys.exit()
		if o == '-c':
			filename = a
		if o == '-g':
			overwrite.append(a.split('='))
		if o == '-d':
			path = a
	for o, a in overwrite:
		# for -g right now I only expected to change intp_size, will add more options later if necessary
		if o == 'intp_size':
			interposer_size = float(a)

	config = configparser.ConfigParser()
	config.read(filename)

	if not path:
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
		if interposer_size == 0:
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

def usage():
	print ('Usage:')
	print ('%s -d <outputdir> -c <config-file> -g <options>' % sys.argv[0])
	sys.exit(2)

def parse_command():
	try:
		opts, args = getopt.getopt(sys.argv[1:], "hc:d:g:")
	except getopt.GetoptError as err:
		print (err)
		usage()
	return opts

if __name__ == "__main__":
	system = read_config()
	print (system.chiplet_count, system.intp_size, system.power, system.x)
