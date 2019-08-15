# script for submitting jobs
import os


cases = ['40', '50', 'small']
iterations = 5

for c in cases:
	for i in range(iterations):
		with open ('run_'+c+'_'+str(i)+'.sh', 'w') as RUN:
			RUN.write('#!/bin/bash -l\n')
			RUN.write('#$ -N run_'+c+'_'+str(i)+'\n#$ -j y \n\n')
			RUN.write('module load python3/3.6.5\n')
			RUN.write('time python sim_annealing.py -d outputs/run_'+c+'_'+str(i)+'/ ')
			if c == '50':
				RUN.write('-g intp_size=50 ')
			elif c == 'small':
				RUN.write('-c small_chiplet.cfg ')
			RUN.write('\n')
		os.system('qsub run_'+c+'_'+str(i)+'.sh')