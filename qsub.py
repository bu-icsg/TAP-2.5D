# script for submitting jobs
import os


# cases = ['40', '50', 'small', 'homo_ring']
cases = ['homo_ring','homo_donut']
link_types = ['nppl','ppl']
multi_start = 10

for c in cases:
	for ltype in link_types:
		for i in range(multi_start):
			with open ('run_'+c+'_'+ltype+str(i)+'.sh', 'w') as RUN:
				RUN.write('#!/bin/bash -l\n')
				RUN.write('#$ -N run_'+c+'_'+ltype+str(i)+'\n#$ -j y \n\n')
				RUN.write('module load python3/3.6.5\n')
				RUN.write('module load cplex/12.8_ac\n')
				RUN.write('time python sim_annealing.py -d outputs/Oct07/run_'+c+'_'+ltype+str(i)+'/24/ -g link_type='+ltype+' ')
				if c == '50':
					RUN.write('-g intp_size=50 ')
				elif c == 'small':
					RUN.write('-c small_chiplet.cfg ')
				elif c == 'homo_ring' or c == 'homo_donut':
					RUN.write('-c '+c+'.cfg')
				RUN.write('\n')
			os.system('qsub -l h_rt=24:00:00 -o run_'+c+'_'+ltype+str(i)+'.o run_'+c+'_'+ltype+str(i)+'.sh')