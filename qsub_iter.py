# script for submitting jobs
import os, time

# cases = ['40', '50', 'small', 'homo_ring']
cases = ['homo_ring','homo_donut']
link_types = ['nppl','ppl']
multi_start = 10
intp_size = 26

for c in cases:
	for ltype in link_types:
		for i in range(multi_start):
			for intp_size in range(28,51,2):
				path = 'outputs/Oct07/run_'+c+'_'+ltype+str(i)+'/'
				if os.path.exists(path+str(intp_size)+'/') or os.path.isfile('run_'+c+'_'+ltype+str(i)+'_'+str(intp_size)+'.sh'):
					continue
				elif os.path.isfile(path+str(intp_size - 2)+'/output.txt'):
					with open(path + str(intp_size-2) + '/output.txt','r') as OUTPUT:
						for _ in range(3):
							OUTPUT.readline()
						x = ''.join(OUTPUT.readline().split())[1:-1]
						y = ''.join(OUTPUT.readline().split())[1:-1]
					with open ('run_'+c+'_'+ltype+str(i)+'_'+str(intp_size)+'.sh', 'w') as RUN:
						RUN.write('#!/bin/bash -l\n')
						RUN.write('#$ -N run_'+c+'_'+ltype+str(i)+'_'+str(intp_size)+'\n#$ -j y \n\n')
						RUN.write('module load python3/3.6.5\n')
						RUN.write('module load cplex/12.8_ac\n')
						RUN.write('time python sim_annealing.py -d '+path+str(intp_size)+'/ -g link_type='+ltype+' -g intp_size='+str(intp_size)+' -g x='+x+' -g y='+y+' ')
						if c == 'small':
							RUN.write('-c small_chiplet.cfg ')
						elif c == 'homo_ring' or c == 'homo_donut':
							RUN.write('-c '+c+'.cfg')
						RUN.write('\n')
					os.system('qsub -l h_rt=24:00:00 -o run_'+c+'_'+ltype+str(i)+'_'+str(intp_size)+'.o run_'+c+'_'+ltype+str(i)+'_'+str(intp_size)+'.sh')
					# print('qsub -l h_rt=24:00:00 -o run_'+c+'_'+ltype+str(i)+'_'+str(intp_size)+'.o run_'+c+'_'+ltype+str(i)+'_'+str(intp_size)+'.sh')
				elif os.path.isfile(path+str(intp_size - 4)+'/output.txt'):
					with open(path + str(intp_size-4) + '/output.txt','r') as OUTPUT:
						for _ in range(3):
							OUTPUT.readline()
						x = ''.join(OUTPUT.readline().split())[1:-1]
						y = ''.join(OUTPUT.readline().split())[1:-1]
					with open ('run_'+c+'_'+ltype+str(i)+'_'+str(intp_size)+'.sh', 'w') as RUN:
						RUN.write('#!/bin/bash -l\n')
						RUN.write('#$ -N run_'+c+'_'+ltype+str(i)+'_'+str(intp_size)+'\n#$ -j y \n\n')
						RUN.write('module load python3/3.6.5\n')
						RUN.write('module load cplex/12.8_ac\n')
						RUN.write('time python sim_annealing.py -d '+path+str(intp_size)+'/ -g link_type='+ltype+' -g intp_size='+str(intp_size)+' -g x='+x+' -g y='+y+' ')
						if c == 'small':
							RUN.write('-c small_chiplet.cfg ')
						elif c == 'homo_ring' or c == 'homo_donut':
							RUN.write('-c '+c+'.cfg')
						RUN.write('\n')
					os.system('qsub -l h_rt=24:00:00 -o run_'+c+'_'+ltype+str(i)+'_'+str(intp_size)+'.o run_'+c+'_'+ltype+str(i)+'_'+str(intp_size)+'.sh')
					# print('qsub -l h_rt=24:00:00 -o run_'+c+'_'+ltype+str(i)+'_'+str(intp_size)+'.o run_'+c+'_'+ltype+str(i)+'_'+str(intp_size)+'.sh')

print ('sleep')
time.sleep(600)
os.system('qsub autosubmit.sh')

