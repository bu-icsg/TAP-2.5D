import configparser
import getopt
import os, sys, time
from passive_interposer import PassiveInterposer
import routing

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
	link_type = None
	x, y = None, None
	decay, weight = None, None
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
		if o == 'link_type':
			link_type = a
		if o == 'x':
			x = a
		if o == 'y':
			y = a
		if o == 'decay':
			decay = float(a)
		if o == 'weight':
			weight = a

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
		init_place_option = 'bstree'
	if init_place_option == 'given':
		if x == None:
			chiplet_x = get_list(config.get('chiplets', 'x'))
		else:
			chiplet_x = list(map(float, x.split(',')))
		if y == None:
			chiplet_y = get_list(config.get('chiplets', 'y'))
		else:
			chiplet_y = list(map(float, y.split(',')))
	else:
		chiplet_x, chiplet_y = [], []

	if decay == None:
		try:
			decay = config.getfloat('general', 'decay')
		except:
			decay = 0.8
	if weight == None:
		try:
			weight = config.git('general', 'weight')
		except:
			weight = 'equal'

	interposer_type = config.get('interposer', 'intp_type')
	assert interposer_type in get_intp_types(), 'only support for passive interposer so far (to update with active, photonic, and EMIB options)'

	chiplet_count = config.getint('chiplets', 'chiplet_count')
	chiplet_width = get_list(config.get('chiplets', 'widths'))
	chiplet_height = get_list(config.get('chiplets', 'heights'))
	chiplet_power = get_list(config.get('chiplets', 'powers'))
	chiplet_connection = get_matrix(config.get('chiplets', 'connections'))

	if interposer_type == 'passive':
		if link_type == None:
			try:
				link_type = config.get('interposer', 'link_type')
			except:
				link_type = 'nppl'
		if interposer_size == 0:
			interposer_size = config.getfloat('interposer', 'intp_size')
		system = PassiveInterposer()
		system.set_path(path)
		if os.path.exists(path) == False:
			os.system('mkdir -p ' + path)
		system.set_decay_factor(decay)
		system.set_weight_option(weight)
		system.set_chiplet_count(chiplet_count)
		system.initialize()
		system.set_interposer_type(interposer_type)
		system.set_link_type(link_type)
		system.set_interposer_size(interposer_size)
		system.set_chiplet_power(chiplet_power)
		system.set_chiplet_size(chiplet_width, chiplet_height)
		system.set_connection_matrix(chiplet_connection)
		system.compute_ubump_overhead()
		system.set_granularity(granularity)
		system.initial_placement(init_place_option, chiplet_x, chiplet_y)

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
	print (system.connection_matrix)
	filename = system.path.split('/')[-2]
	print (system.path)
	print (filename)
	start_time = time.time()
	system.gen_flp(filename)
	system.gen_ptrace(filename)
	temp = system.run_hotspot(filename)
	os.system('perl util/grid_thermal_map.pl ' + system.path+filename+'L4_ChipLayer.flp '+system.path + filename + '.grid.steady > '+system.path+filename+'.svg')
	os.system('convert '+system.path + filename + '.svg '+system.path + filename + '.pdf')
	print (temp, 'C,    takes ', time.time()- start_time)

	start_time = time.time()
	length = routing.solve_Cplex(system)
	print (length, 'mm,    takes ', time.time() - start_time)
	with open (system.path + filename +  '.txt', 'w') as OUTPUT:
		OUTPUT.write(str(temp)+'\n')
		OUTPUT.write(str(length)+'\n')
