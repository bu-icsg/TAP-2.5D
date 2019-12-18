# script for submitting jobs
import os, sys, random

def qsub():
	if len(sys.argv)>1:
		start_point = int(sys.argv[1])
	else:
		start_point = 0

	num_systems = 100
	n = 0
	for syst in range(3):
		c = 'rand' + str(syst)
		for ltype in link_types:
			for weight in weights:
				for decay in decay_factors:
					for intp_size in intp_sizes:
						i = start_point
						path = 'outputs/Dec2019/' + c + '/' + ltype + '/' + weight + '/' + str(decay) + '/' + str(intp_size) + '/' + str(i) + '/'
						run_name = c+'_'+ltype+'_'+weight + '_'+str(decay)+'_'+str(intp_size)+'_'+str(i)
						print (path)
						os.system('mkdir -p ' + path)
						if os.path.isfile(path + 'run_'+run_name + '.sh') == False:
							with open (path + 'run_'+run_name+'.sh', 'w') as RUN:
								RUN.write('#!/bin/bash -l\n')
								RUN.write('#$ -N run_'+run_name+'\n#$ -j y \n\n')
								RUN.write('module load python3/3.6.5\n')
								RUN.write('module load cplex/12.8_ac\n')
								RUN.write('time python sim_annealing.py -d '+path +' -c configs/sys_'+c+'.cfg -g link_type='+ltype+' -g weight='+weight+' -g decay='+str(decay)+' -g intp_size='+str(intp_size)+'\n')
							os.system('qsub -l h_rt=100:00:00 -o '+path + 'run_'+run_name+'.o ' + path + 'run_'+run_name+'.sh')
							n += 1
	print ('submit ', n, ' new jobs')

def random_sys_generator():
	if len(sys.argv) > 1:
		num_systems = int(sys.argv[1])
	else:
		num_systems = 1
	for syst in range(num_systems):
		c = 'rand' + str(syst)
		for ltype in link_types:
			for weight in weights:
				for decay in decay_factors:
					for intp_size in intp_sizes:
						chiplet_count = random.randint(2,8)
						widths, heights, powers = [], [], []
						connections = [[0 for _ in range(chiplet_count)] for _ in range(chiplet_count)]
						for i in range(chiplet_count):
							w = random.randint(10, 200) / 10
							h = random.randint(10, 200) / 10
							while w/h < 0.5 or w/h >2:
								w = random.randint(10, 200) / 10
								h = random.randint(10, 200) / 10
							p = int(random.random() * 2 * w * h * 10) / 10
							widths.append(w)
							heights.append(h)
							powers.append(p)
						num_conn = random.randint(chiplet_count, int(chiplet_count*chiplet_count / 2))
						for i in range(num_conn):
							s, t = random.randint(0, chiplet_count - 1), random.randint(0, chiplet_count - 1)
							while s == t:
								s, t = random.randint(0, chiplet_count - 1), random.randint(0, chiplet_count - 1)
							bw = random.randint(1, 8) * 128
							connections[s][t] = bw
							connections[t][s] = bw

						path = 'configs/'
						# if os.path.isfile(path + 'sys_'+c + '.cfg') == False:
						if True:
							with open (path + 'sys_'+c+'.cfg', 'w') as CONFIG:
								CONFIG.write('[general]\n')
								CONFIG.write('path = /projectnb/photonoc/yenai/hetero-placer/Dec2019/\n')
								CONFIG.write('placer_granularity = 1\n')
								CONFIG.write('initial_placement = bstree\n')
								CONFIG.write('decay = 0.8\n\n')
								CONFIG.write('[interposer]\n')
								CONFIG.write('intp_type = passive\n')
								CONFIG.write('intp_size = 50\n')
								CONFIG.write('link_type = nppl\n\n')
								CONFIG.write('[chiplets]\n')
								CONFIG.write('chiplet_count = '+ str(chiplet_count)+'\n')
								CONFIG.write('widths = '+','.join(map(str, widths))+'\n')
								CONFIG.write('heights = '+','.join(map(str, heights))+'\n')
								CONFIG.write('powers = '+','.join(map(str, powers))+'\n')
								CONFIG.write('connections = ')
								for i in range(chiplet_count-1):
									CONFIG.write('\t'+','.join(map(str, connections[i])) + ';\n')
								CONFIG.write('\t'+','.join(map(str, connections[chiplet_count - 1]))+'\n')

cases = ['ascend910','multigpu','micro150','micro125','micro100','micro75']   #,'topo_a','topo_b','topo_c','topo_d'
link_types = ['nppl', 'ppl']
weights = ['adpTWv2']		# not going to run adpT, not perform well. adpTWh also covers the same concept as adpTW, but amend the issue in low temp region. 'equal',
intp_sizes = [50, 45]		 # and 40
decay_factors = [0.8, 0.85, 0.9, 0.95]    # and 0.95

qsub()
# random_sys_generator()
# autocheck()