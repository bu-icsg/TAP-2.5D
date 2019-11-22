# script for submitting jobs
import os

start_point = 1
cases = ['ascend910','multigpu','micro150','micro125','micro100','micro75','micro50']
link_types = ['nppl', 'ppl']
weights = ['equal', 'adpT', 'adpTW']		
intp_sizes = [50]		 # and 40
decay_factors = [0.8, 0.85, 0.9, 0.95]    # and 0.95

for c in cases:
	for ltype in link_types:
		for weight in weights:
			for decay in decay_factors:
				for intp_size in intp_sizes:
					i = start_point
					path = 'outputs/Nov21/' + c + '/' + ltype + '/' + weight + '/' + str(decay) + '/' + str(intp_size) + '/' + str(i) + '/'
					run_name = c+'_'+ltype+'_'+weight + '_'+str(decay)+'_'+str(intp_size)+'_'+str(i)
					if os.path.isfile('run_'+run_name + '.sh') == False:
						with open ('run_'+run_name+'.sh', 'w') as RUN:
							RUN.write('#!/bin/bash -l\n')
							RUN.write('#$ -N run_'+run_name+'\n#$ -j y \n\n')
							RUN.write('module load python3/3.6.5\n')
							RUN.write('module load cplex/12.8_ac\n')
							RUN.write('time python sim_annealing.py -d '+path +' -c sys_'+c+'.cfg -g link_type='+ltype+' -g weight='+weight+' -g decay='+str(decay)+' -g intp_size='+str(intp_size)+'\n')
						os.system('qsub -l h_rt=100:00:00 -o run_'+run_name+'.o run_'+run_name+'.sh')