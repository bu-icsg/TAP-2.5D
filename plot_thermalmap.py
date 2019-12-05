import os

def plot():
	path_root = 'outputs/Nov21/plots/'+case + '/45mm/'
	plots = ['a_layout', 'b_bstree', 'c_npplsol', 'd_pplsol']
	temp_arg = str(min_temp + 273.15) + ' ' + str(max_temp + 273.15)
	for plot in plots:
		path = path_root + plot + '/'
		if os.path.exists(path):
			os.system('perl util/grid_thermal_map.pl ' + path + plot + 'L4_ChipLayer.flp ' + path + plot + '.grid.steady 64 64 '+temp_arg+' > '+path_root+plot+'_scale.svg')
			os.system('convert '+path_root + plot + '_scale.svg '+path_root + plot + '_scale.pdf')

# cases = ['ascend910', 'micro150', 'multigpu']
case = 'multigpu'
max_temp = 97.5
min_temp = 61.7

plot()

