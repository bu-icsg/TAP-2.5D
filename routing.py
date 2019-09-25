import cplex
import sys, time
from copy import deepcopy

def read_input():
	'''
	This function is only for replicating the in/outs of Vaishnav's version. 
	For testing purpose only.
	To interface with the rest of the tool, need to use config function
	'''
	if len(sys.argv) > 1:
		path = sys.argv[1]
	else:
		path = ''

	with open(path + 'OptPlaceRoute.cfg', 'r') as Conf:
		Conf.readline()
		Conf.readline()
		Conf.readline()
		Nclump = int(Conf.readline().split()[1])
		Nchiplet = int(Conf.readline().split()[1])
		p = int(Conf.readline().split()[1])
		Hopmax = int(Conf.readline().split()[1])
	pmax = [[p for h in range(Nclump)] for i in range(Nchiplet)]

	xl, yl = [0] * Nchiplet, [0] * Nchiplet
	xc, yc = [[0 for h in range(Nclump)] for i in range(Nchiplet)], [[0 for h in range(Nclump)] for i in range(Nchiplet)]
	R = [[0 for i in range(Nchiplet)] for j in range(Nchiplet)]
	with open(path + 'Xl.txt', 'r') as Xchiplet:
		for i in range(Nchiplet):
			xl[i] = float(Xchiplet.readline())
	with open(path + 'Xc.txt', 'r') as Xclump:
		for h in range(Nclump):
			p = float(Xclump.readline())
			for i in range(Nchiplet):
				xc[i][h] = p
	with open(path + 'Yl.txt', 'r') as Ychiplet:
		for i in range(Nchiplet):
			yl[i] = float(Ychiplet.readline())
	with open(path + 'Yc.txt', 'r') as Yclump:
		for h in range(Nclump):
			p = float(Yclump.readline())
			for i in range(Nchiplet):
				yc[i][h] = p
	with open(path + 'R.txt', 'r') as Connection:
		for i in range(Nchiplet):
			R[i] = list(map(int,Connection.readline().split()))

	print (R)
	return xl, xc, yl, yc, R, Nchiplet, Nclump, pmax, Hopmax

def get_input(system):
	# to account for heterogeneous chiplet, the xc, yc, pmax are 2d array now. index [i][h] indicates chiplet i pin clump h
	Nclump = 4
	Nchiplet = system.chiplet_count
	Hopmax = 1
	ubump_pitch = 0.045 # 45um in unit of mm
	if system.intp_type == 'passive':
		if system.link_type == 'ppl':
			Hopmax = 2
	# xl, yl here are locations of the bottem-left corner of chiplets (this way the offset xc, yc will be positive)
	xl, yl = [None] * Nchiplet, [None] * Nchiplet
	# xc, yc are the offset of the pin clump to the center of chiplet
	xc, yc, pmax = [[None for h in range(Nclump)] for i in range(Nchiplet)],[[None for h in range(Nclump)] for i in range(Nchiplet)],[[None for h in range(Nclump)] for i in range(Nchiplet)]
	for i in range(Nchiplet):
		xl[i], yl[i] = system.x[i] - system.width[i] / 2 - system.hubump[i], system.y[i] - system.height[i] / 2 - system.hubump[i]
		xc[i][0], yc[i][0], pmax[i][0] = system.hubump[i] / 2, system.height[i] / 2 + system.hubump[i], int(system.hubump[i] / ubump_pitch) * int((system.height[i]+system.hubump[i]) / ubump_pitch)
		xc[i][1], yc[i][1], pmax[i][1] = system.width[i] / 2 + system.hubump[i], system.hubump[i] * 1.5 + system.height[i], int(system.hubump[i] / ubump_pitch) * int((system.width[i] + system.hubump[i]) / ubump_pitch)
		xc[i][2], yc[i][2], pmax[i][2] = system.width[i] + system.hubump[i] * 1.5, yc[i][0], pmax[i][0]
		xc[i][3], yc[i][3], pmax[i][3] = xc[i][1], system.hubump[i] / 2, pmax[i][1]
	R = deepcopy(system.connection_matrix)
	return xl, xc, yl, yc, R, Nchiplet, Nclump, pmax, Hopmax

def translate_index(f_index, Nchiplet, Nclump, Nmax):
	index = int(f_index / 2)
	n = index % Nmax
	index = int((index - n) / Nmax)
	k = index % Nclump
	index = int((index - k) / Nclump)
	j = index % Nchiplet
	index = int((index - j) / Nchiplet)
	h = index % Nclump
	i = int((index - h) / Nclump)
	return i, h, j, k, n

def get_index(i, h, j, k, n, Nchiplet, Nclump, Nmax):
	f_index = (i * Nclump * Nchiplet * Nclump * Nmax + h * Nchiplet * Nclump * Nmax + j * Nclump * Nmax + k * Nmax + n) * 2
	return f_index

def solve_Cplex(system):
	# read from previous inout files for testing purpose, later we read from system class
	# xl, xc, yl, yc, R, Nchiplet, Nclump, pmax, Hopmax = read_input()
	xl, xc, yl, yc, R, Nchiplet, Nclump, pmax, Hopmax = get_input(system)

	problem = cplex.Cplex()
	problem.objective.set_sense(problem.objective.sense.minimize)
	problem.parameters.threads.set(1)
	# problem.parameters.tuning.timelimit.set(300.0)

	# calculate d
	start_time = time.time()
	d = [[[[0 for _ in range(Nclump)] for _ in range(Nchiplet)] for _ in range(Nclump)] for _ in range(Nchiplet)]
	for i in range(Nchiplet):
		for h in range(Nclump):
			for j in range(Nchiplet):
				for k in range(Nclump):
					d[i][h][j][k] = abs(xl[i] + xc[i][h] - xl[j] - xc[j][k]) + abs(yl[i] + yc[i][h] - yl[j] - yc[j][k])
	# print ('time to initialize d', time.time() - start_time)
	start_time = time.time()
	# get sn, tn pair
	s, t = [], []
	n = 0
	for i in range(Nchiplet):
		for j in range(Nchiplet):
			if (i!=j) and (R[i][j]>0):
				s.append(i)
				t.append(j)
				n += 1
	Nmax = n
	# print ('time to initialize s,t', time.time() - start_time)
	start_time = time.time()

	# Eq. 11. initialize f[i][h][j][k][n] and set lower bound 0
	for i in range(Nchiplet):
		for h in range(Nclump):
			for j in range(Nchiplet):
				for k in range(Nclump):
					for n in range(Nmax):
						if (i==j) and (h==k):
							problem.variables.add(lb = [0.0, 0.0], ub = [0.0, 0.0], types = [problem.variables.type.integer]*2)
						else:
							problem.variables.add(lb = [0.0, 0.0], ub = [pmax[i][h], 1.0], types = [problem.variables.type.integer]*2)
	# print ('time to initialize decision variables f and lambda', time.time() - start_time)
	start_time = time.time()

	num_val = problem.variables.get_num()
	# print (num_val)

	# print ('time to get variable count', time.time() - start_time)
	start_time = time.time()

	# Eq. 12
	for n in range(Nmax):
		row_index, row_coeff = [], []
		for h in range(Nclump):
			for j in range(Nchiplet):
				if j != s[n]: # This is to make sure there is no duplicate indices which raises an exception.
					for k in range(Nclump):
						# fij_index = (s[n] * Nclump * Nchiplet * Nclump * Nmax + h * Nchiplet * Nclump * Nmax + j * Nclump * Nmax + k * Nmax + n) * 2
						fij_index = get_index(s[n], h, j, k, n, Nchiplet, Nclump, Nmax)
						row_index.append(fij_index)
						row_coeff.append(1)
						# fji_index = (j * Nclump * Nchiplet * Nclump * Nmax + k * Nchiplet * Nclump * Nmax + s[n] * Nclump * Nmax + h * Nmax + n) * 2
						fji_index = get_index(j, k, s[n], h, n, Nchiplet, Nclump, Nmax)
						row_index.append(fji_index)
						row_coeff.append(-1)
		problem.linear_constraints.add(lin_expr = [[row_index, row_coeff]], senses = ["E"], rhs = [R[s[n]][t[n]]])

		row_index, row_coeff = [], []
		for h in range(Nclump):
			for j in range(Nchiplet):
				if j != t[n]: # This is to make sure there is no duplicate indices which raises an exception.
					for k in range(Nclump):
						# fij_index = (t[n] * Nclump * Nchiplet * Nclump * Nmax + h * Nchiplet * Nclump * Nmax + j * Nclump * Nmax + k * Nmax + n) * 2
						fij_index = get_index(t[n], h, j, k, n, Nchiplet, Nclump, Nmax)
						row_index.append(fij_index)
						row_coeff.append(1)
						# fji_index = (j * Nclump * Nchiplet * Nclump * Nmax + k * Nchiplet * Nclump * Nmax + t[n] * Nclump * Nmax + h * Nmax + n) * 2
						fji_index = get_index(j, k, t[n], h, n, Nchiplet, Nclump, Nmax)
						row_index.append(fji_index)
						row_coeff.append(-1)
		problem.linear_constraints.add(lin_expr = [[row_index, row_coeff]], senses = ["E"], rhs = [-R[s[n]][t[n]]])
	
		for i in range(Nchiplet):
			if (i != s[n]) and (i != t[n]):
				row_index, row_coeff = [], []
				for h in range(Nclump):
					for j in range(Nchiplet):
						if j != i: # This is to make sure there is no duplicate indices which raises an exception.
							for k in range(Nclump):
								# fij_index = (i * Nclump * Nchiplet * Nclump * Nmax + h * Nchiplet * Nclump * Nmax + j * Nclump * Nmax + k * Nmax + n) * 2
								fij_index = get_index(i, h, j, k, n, Nchiplet, Nclump, Nmax)
								row_index.append(fij_index)
								row_coeff.append(1)
								# fji_index = (j * Nclump * Nchiplet * Nclump * Nmax + k * Nchiplet * Nclump * Nmax + i * Nclump * Nmax + h * Nmax + n) * 2
								fji_index = get_index(j, k, i, h, n, Nchiplet, Nclump, Nmax)
								row_index.append(fji_index)
								row_coeff.append(-1)
				problem.linear_constraints.add(lin_expr = [[row_index, row_coeff]], senses = ["E"], rhs = [0])

	# print ('time to Formulate Eq.12:', time.time() - start_time)
	start_time = time.time()

	# Eq.13 and Eq. 14
	for n in range(Nmax):
		srow_index, srow_coeff = [], []
		trow_index, trow_coeff = [], []
		for h in range(Nclump):
			for j in range(Nchiplet):
				for k in range(Nclump):
					# fs_index = (j * Nclump * Nchiplet * Nclump * Nmax + k * Nchiplet * Nclump * Nmax + s[n] * Nclump * Nmax + h * Nmax + n) * 2
					fs_index = get_index(j, k, s[n], h, n, Nchiplet, Nclump, Nmax)
					srow_index.append(fs_index)
					srow_coeff.append(1)
					# ft_index = (t[n] * Nclump * Nchiplet * Nclump * Nmax + h * Nchiplet * Nclump * Nmax + j * Nclump * Nmax + k * Nmax + n) * 2
					ft_index = get_index(t[n], h, j, k, n, Nchiplet, Nclump, Nmax)
					trow_index.append(ft_index)
					trow_coeff.append(1)
		problem.linear_constraints.add(lin_expr = [[srow_index, srow_coeff]], senses = ["E"], rhs = [0])
		problem.linear_constraints.add(lin_expr = [[trow_index, trow_coeff]], senses = ["E"], rhs = [0])

	# print ('time to formulate 13 and 14:', time.time() - start_time)
	start_time = time.time()

	# Eq.15
	for i in range(Nchiplet):
		for h in range(Nclump):
			row_index, row_coeff = [], []
			for j in range(Nchiplet):
				if i != j:
					for k in range(Nclump):
						for n in range(Nmax):
							# fij_index = (i * Nclump * Nchiplet * Nclump * Nmax + h * Nchiplet * Nclump * Nmax + j * Nclump * Nmax + k * Nmax + n) * 2
							fij_index = get_index(i, h, j, k, n, Nchiplet, Nclump, Nmax)
							row_index.append(fij_index)
							row_coeff.append(1)
							# fji_index = (j * Nclump * Nchiplet * Nclump * Nmax + k * Nchiplet * Nclump * Nmax + i * Nclump * Nmax + h * Nmax + n) * 2
							fji_index = get_index(j, k, i, h, n, Nchiplet, Nclump, Nmax)
							row_index.append(fji_index)
							row_coeff.append(1)
			problem.linear_constraints.add(lin_expr = [[row_index, row_coeff]], senses = ["L"], rhs = [pmax[i][h]])
	# print ('time to Formulate Eq.15:', time.time() - start_time)
	start_time = time.time()

	# Eq. 16
	for i in range(Nchiplet):
		for h in range(Nclump):
			for j in range(Nchiplet):
				for k in range(Nclump):
					for n in range(Nmax):
						# f_index = (i * Nclump * Nchiplet * Nclump * Nmax + h * Nchiplet * Nclump * Nmax + j * Nclump * Nmax + k * Nmax + n) * 2
						f_index = get_index(i, h, j, k, n, Nchiplet, Nclump, Nmax)
						problem.indicator_constraints.add(indvar = f_index + 1, rhs = 1.0, sense = "G", lin_expr = [[f_index], [1.0]], indtype = 3)
	# print (problem.indicator_constraints.get_num())
	# print ('time to Formulate Eq.16:', time.time() - start_time)
	start_time = time.time()

	# Eq. 17
	problem.variables.add(lb = [0.0], ub = [100.0], types = [problem.variables.type.integer])
	for i in range(Nchiplet):
		for h in range(Nclump):
			for j in range(Nchiplet):
				for k in range(Nclump):
					for n in range(Nmax):
						# f_index = (i * Nclump * Nchiplet * Nclump * Nmax + h * Nchiplet * Nclump * Nmax + j * Nclump * Nmax + k * Nmax + n) * 2 + 1
						f_index = get_index(i, h, j, k, n, Nchiplet, Nclump, Nmax) + 1
						problem.linear_constraints.add(lin_expr=[[[f_index, num_val],[-d[i][h][j][k], 1]]], senses = ["G"], rhs = [0.0])
	# print ('time to Formulate Eq.17:', time.time() - start_time)
	start_time = time.time()

	# Eq. 18
	for n in range(Nmax):
		row_index, row_coeff = [], []
		if Hopmax == 1:
			for i in range(Nchiplet):
				for h in range(Nclump):
					for j in range(Nchiplet):
						for k in range(Nclump):
							# f_index = (i * Nclump * Nchiplet * Nclump * Nmax + h * Nchiplet * Nclump * Nmax + j * Nclump * Nmax + k * Nmax + n) * 2
							f_index = get_index(i, h, j, k, n, Nchiplet, Nclump, Nmax)
							row_index.append(f_index)
							row_coeff.append(1)
			problem.linear_constraints.add(lin_expr = [[row_index, row_coeff]], senses = ["L"], rhs = [R[s[n]][t[n]]])
		elif Hopmax == 2:
			for h in range(Nclump):
				for k in range(Nclump):
					# f_index = (s[n] * Nclump * Nchiplet * Nclump * Nmax + h * Nchiplet * Nclump * Nmax + t[n] * Nclump * Nmax + k * Nmax + n) * 2
					f_index = get_index(s[n], h, t[n], k, n, Nchiplet, Nclump, Nmax)
					row_index.append(f_index)
					row_coeff.append(2)
					for i in range(Nchiplet):
						for j in range(Nchiplet):
							if i!=s[n] or j!=t[n]:
								# f_index = (i * Nclump * Nchiplet * Nclump * Nmax + h * Nchiplet * Nclump * Nmax + j * Nclump * Nmax + k * Nmax + n) * 2
								f_index = get_index(i, h, j, k, n, Nchiplet, Nclump, Nmax)
								row_index.append(f_index)
								row_coeff.append(1)
			problem.linear_constraints.add(lin_expr = [[row_index, row_coeff]], senses = ["L"], rhs = [2 * R[s[n]][t[n]]])
		# elif Hopmax == 3:
		# 	for h in range(Nclump):
		# 		for k in range(Nclump):
		# 			f_index = (s[n] * Nclump * Nchiplet * Nclump * Nmax + h * Nchiplet * Nclump * Nmax + t[n] * Nclump * Nmax + k * Nmax + n) * 2
		# 			row_index.append(f_index)
		# 			row_coeff.append(2)
		# 	problem.linear_constraints.add(lin_expr = [[row_index, row_coeff]], senses = ["L"], rhs = [3 * R[s[n]][t[n]]])

	# print ('time to Formulate Eq.18:', time.time() - start_time)
	start_time = time.time()

	problem.objective.set_linear(num_val, 1.0)
	# print (problem.objective.get_linear())

	problem.solve()	
	# print('time to solve cplex:', time.time() - start_time)

	# for f_index,x in enumerate(problem.solution.get_values()[:-1]):
	# 	if x!=0 and f_index % 2 == 0:
	# 		i, h, j, k, n = translate_index(f_index, Nchiplet, Nclump, Nmax)
	# 		print (f_index, i, h, j, k, n, x, d[i][h][j][k])

	# for n in range(Nmax):
	# 	print (n, s[n], t[n])
		
	print ('Maximum wire Length: ', problem.solution.get_values()[-1])
	return problem.solution.get_values()[-1]

if __name__ == "__main__":
	solve_Cplex()