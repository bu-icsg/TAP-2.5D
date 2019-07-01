import ConfigParser

config = ConfigParser.ConfigParser()
config.read('example.cfg')

path = config.get('taco', 'path')
system = config.get('taco', 'system')
assert system == '2.5D', 'only support 2.5D system!'
n_chiplet_type = config.getint('2.5D', 'n_chiplet_type')
n_chiplet, width, height, power = [0] * n_chiplet_type, [0] * n_chiplet_type, [0] * n_chiplet_type, [0] * n_chiplet_type
for i in range(n_chiplet_type):
	n_chiplet[i] = config.getint('2.5D', 'n_chiplet_'+str(i))
	width[i] = config.getfloat('2.5D', 'width_'+str(i))
	height[i] = config.getfloat('2.5D', 'height_'+str(i))
	power[i] = config.getfloat('2.5D', 'power_'+str(i))

print n_chiplet
print width
print height
print power

