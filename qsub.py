# script for submitting jobs
import os, sys

if len(sys.argv)>1:
	start_point = int(sys.argv[1])
else:
	start_point = 12

cases = ['ascend910','multigpu','micro150','micro125','micro100','micro75']   #,'topo_a','topo_b','topo_c','topo_d'
link_types = ['nppl', 'ppl']
weights = ['adpTWv2']		# not going to run adpT, not perform well. adpTWh also covers the same concept as adpTW, but amend the issue in low temp region. 'equal',
intp_sizes = [50, 45]		 # and 40
decay_factors = [0.8, 0.85, 0.9, 0.95]    # and 0.95

n = 0
for c in cases:
	for ltype in link_types:
		for weight in weights:
			for decay in decay_factors:
				for intp_size in intp_sizes:
					i = start_point
					path = 'outputs/Nov21/' + c + '/' + ltype + '/' + weight + '/' + str(decay) + '/' + str(intp_size) + '/' + str(i) + '/'
					run_name = c+'_'+ltype+'_'+weight + '_'+str(decay)+'_'+str(intp_size)+'_'+str(i)
					print (path)
					if os.path.isfile('run_'+run_name + '.sh') == False:
						with open ('run_'+run_name+'.sh', 'w') as RUN:
							RUN.write('#!/bin/bash -l\n')
							RUN.write('#$ -N run_'+run_name+'\n#$ -j y \n\n')
							RUN.write('module load python3/3.6.5\n')
							RUN.write('module load cplex/12.8_ac\n')
							RUN.write('time python sim_annealing.py -d '+path +' -c configs/sys_'+c+'.cfg -g link_type='+ltype+' -g weight='+weight+' -g decay='+str(decay)+' -g intp_size='+str(intp_size)+'\n')
						os.system('qsub -l h_rt=72:00:00 -o run_'+run_name+'.o run_'+run_name+'.sh')
						n += 1
print ('submit ', n, ' new jobs')