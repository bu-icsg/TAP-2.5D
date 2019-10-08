# script for submitting jobs
import os


# cases = ['40', '50', 'small', 'homo_ring']
cases = ['homo_ring','homo_donut']
link_types = ['nppl','ppl']
multi_start = 10
intp_size = 24

for c in cases:
	for ltype in link_types:
		for i in range(multi_start):
			with open ('run_'+c+'_'+ltype+str(i)+'_'+str(intp_size)+'.sh', 'w') as RUN:
				RUN.write('#!/bin/bash -l\n')
				RUN.write('#$ -N run_'+c+'_'+ltype+str(i)+'_'+str(intp_size)+'\n#$ -j y \n\n')
				RUN.write('module load python3/3.6.5\n')
				RUN.write('module load cplex/12.8_ac\n')
				RUN.write('time python sim_annealing.py -d outputs/Oct07/run_'+c+'_'+ltype+str(i)+'/'+str(intp_size)+'/ -g link_type='+ltype+' -g intp_size='+str(intp_size)+' ' )
				if c == 'small':
					RUN.write('-c small_chiplet.cfg ')
				elif c == 'homo_ring' or c == 'homo_donut':
					RUN.write('-c '+c+'.cfg')
				RUN.write('\n')
			os.system('qsub -l h_rt=24:00:00 -o run_'+c+'_'+ltype+str(i)+'_'+str(intp_size)+'.o run_'+c+'_'+ltype+str(i)+'_'+str(intp_size)+'.sh')