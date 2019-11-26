# script for submitting jobs
import os

start_points = range(10)
cases = ['ascend910','multigpu','micro150','micro125','micro100','micro75','micro50']  #,'topo_a','topo_b','topo_c','topo_d'
link_types = ['nppl', 'ppl']
weights = ['adpTWv2']		# 'equal', 'adpT', 'adpTW', 
intp_sizes = [50, 45]		 # and 40
decay_factors = [0.8, 0.85, 0.9, 0.95]    # and 0.95

def check_status():
	yes = 0
	pending = 0
	with open ('outputs/Nov21/status.csv', 'w') as STATUS:
		STATUS.write('Case, link_type, Weight, Decay, intp_size, start_point, Finish?, complete_step, best_step, temp, length\n')
		for c in cases:
			for ltype in link_types:
				for weight in weights:
					for decay in decay_factors:
						for intp_size in intp_sizes:
							for i in start_points:
								path = 'outputs/Nov21/' + c + '/' + ltype + '/' + weight + '/' + str(decay) + '/' + str(intp_size) + '/' + str(i) + '/'
								run_name = c+'_'+ltype+'_'+weight + '_'+str(decay)+'_'+str(intp_size)+'_'+str(i)
								if os.path.isfile(path + 'output.txt'):
									finish = 'Y'
									yes = yes + 1
								else:
									finish = 'N'
								if os.path.isfile(path + 'log.txt'):
									with open(path + 'log.txt', 'r') as LOG:
										ln = LOG.readline()
										while ln:
											step = int(ln.split()[-1])
											step_best = int(LOG.readline())
											temp_best = float(LOG.readline())
											length_best = float(LOG.readline())
											x_best = list(map(float,LOG.readline()[1:-2].split(',')))
											y_best = list(map(float,LOG.readline()[1:-2].split(',')))
											ln = LOG.readline()
									towrite = ','.join([c, ltype, weight, str(decay), str(intp_size), str(i), finish, str(step), str(step_best), str(temp_best), str(length_best)])
									# print (towrite)
									STATUS.write(towrite+'\n')
									pending += 1
								else:
									towrite = ','.join([c, ltype, weight, str(decay), str(intp_size), str(i), finish])
									STATUS.write(towrite+'\n')
									# print (towrite)
	print ('finished: ', yes)
	print ('running:  ', pending - yes)

def clean():
	for c in cases:
		for ltype in link_types:
			for weight in weights:
				for decay in decay_factors:
					for intp_size in intp_sizes:
						for i in start_points:
							path = 'outputs/Nov21/' + c + '/' + ltype + '/' + weight + '/' + str(decay) + '/' + str(intp_size) + '/' + str(i) + '/'
							run_name = c+'_'+ltype+'_'+weight + '_'+str(decay)+'_'+str(intp_size)+'_'+str(i)
							print (path)
							if os.path.isfile(path + 'output.txt'):
								# with open('clean_' + run_name + '.sh', 'w') as CLEAN:
								# 	CLEAN.write('rm '+path+'step*.pdf\n')
								# 	CLEAN.write('rm ' + path + 'bstree/*/step*\n')
								# os.system('qsub -j y clean_' + run_name + '.sh')
								pass
							else:
								# with open('clean_' + run_name + '.sh', 'w') as CLEAN:
								# 	CLEAN.write('rm -r '+path+'*\n')
								# 	CLEAN.write('rm run_'+run_name+'.*\n')
								# os.system('qsub -j y clean_' + run_name + '.sh -j y')
								pass
								# if os.path.isfile('run_' + run_name +'.sh'):
								# 	os.system('rm -r ' + path + '*')
								# 	os.system('rm run_'+run_name+'.*')
							# else:
								# with open('clean_' + run_name + '.sh', 'w') as CLEAN:
								# 	CLEAN.write('rm '+path+'{*.flp,*.lcf,*.ptrace,*.steady,*ChipLayer.pdf}\n')
								# 	CLEAN.write('rm ' + path + 'bstree/*/step*\n')
								# os.system('qsub -j y clean_' + run_name + '.sh -j y')
								# pass

check_status()
# clean()