import cplex


def read_input():
	'''
	This function is only for replicating the in/outs of Vaishnav's version. 
	For testing purpose only.
	To interface with the rest of the tool, need to use config function
	'''
	xl, xc, yl, yc = [0] * 16, [0] * 4, [0] * 16, [0] * 4
	R = [[0 for i in range(16)] for j in range(16)]
	with open('Xl.txt', 'r') as Xchiplet:
		for i in range(16):
			xl[i] = float(Xchiplet.readline())
	with open('Xc.txt', 'r') as Xclump:
		for i in range(4):
			xc[i] = float(Xclump.readline())
	with open('Yl.txt', 'r') as Ychiplet:
		for i in range(16):
			yl[i] = float(Ychiplet.readline())
	with open('Yc.txt', 'r') as Yclump:
		for i in range(4):
			yc[i] = float(Yclump.readline())
	with open('R.txt', 'r') as Connection:
		for i in range(16):
			R[i] = list(map(int,Connection.readline().split()))
	print (R)
	return xl, xc, yl, yc, R


def solve_Cplex():
	xl, xc, yl, yc, R = read_input()
	# hard code for now, later we read from system class
	Nchiplet, Nclump = 16, 4

	problem = cplex.Cplex()
	problem.objective.set_sense(problem.objective.sense.minimize)
	# problem.parameters.tuning.timelimit.set(300.0)

	# calculate d
	d = [[[[0 for _ in range(Nclump)] for _ in range(Nchiplet)] for _ in range(Nclump)] for _ in range(Nchiplet)]
	for i in range(Nchiplet):
		for h in range(Nclump):
			for j in range(Nchiplet):
				for k in range(Nclump):
					d[i][h][j][k] = abs(xl[i] + xc[h] - xl[j] - xc[k]) + abs(yl[i] + yc[h] - yl[j] - yc[k])
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

	# f = [[[[[0 for _ in range(Nmax)] for _ in range(Nclump)] for _ in range(Nchiplet)] for _ in range(Nclump)] for _ in range(Nchiplet)]
	# lbd = [[[[[0 for _ in range(Nmax)] for _ in range(Nclump)] for _ in range(Nchiplet)] for _ in range(Nclump)] for _ in range(Nchiplet)]

	# Eq. 11. initialize f[i][h][j][k][n] and set lower bound 0
	for i in range(Nchiplet):
		for h in range(Nclump):
			for j in range(Nchiplet):
				for k in range(Nclump):
					for n in range(Nmax):
						if (i!=j) or (h!=k):
							problem.variables.add(lb = [0.0, 0.0], ub = [10000.0, 1.0], types = [problem.variables.type.integer]*2)
						else:
							problem.variables.add(lb = [0.0, 0.0], ub = [0.0, 0.0], types = [problem.variables.type.integer]*2)
	num_val = problem.variables.get_num()
	print (num_val)

	# Eq. 12
	for n in range(Nmax):
		row_index, row_coeff = [], []
		for h in range(Nclump):
			for j in range(Nchiplet):
				if j != s[n]: # This is to make sure there is no duplicate indices which raises an exception.
					for k in range(Nclump):
						fij_index = (s[n] * Nclump * Nchiplet * Nclump * Nmax + h * Nchiplet * Nclump * Nmax + j * Nclump * Nmax + k * Nmax + n) * 2
						row_index.append(fij_index)
						row_coeff.append(1)
						fji_index = (j * Nclump * Nchiplet * Nclump * Nmax + k * Nchiplet * Nclump * Nmax + s[n] * Nclump * Nmax + h * Nmax + n) * 2
						row_index.append(fji_index)
						row_coeff.append(-1)
		problem.linear_constraints.add(lin_expr = [[row_index, row_coeff]], senses = ["E"], rhs = [R[s[n]][t[n]]])

		row_index, row_coeff = [], []
		for h in range(Nclump):
			for j in range(Nchiplet):
				if j != t[n]: # This is to make sure there is no duplicate indices which raises an exception.
					for k in range(Nclump):
						fij_index = (t[n] * Nclump * Nchiplet * Nclump * Nmax + h * Nchiplet * Nclump * Nmax + j * Nclump * Nmax + k * Nmax + n) * 2
						row_index.append(fij_index)
						row_coeff.append(1)
						fji_index = (j * Nclump * Nchiplet * Nclump * Nmax + k * Nchiplet * Nclump * Nmax + t[n] * Nclump * Nmax + h * Nmax + n) * 2
						row_index.append(fji_index)
						row_coeff.append(-1)
		problem.linear_constraints.add(lin_expr = [[row_index, row_coeff]], senses = ["E"], rhs = [-R[s[n]][t[n]]])
	for i in range(Nchiplet):
		if i not in s and i not in t:
			row_index, row_coeff = [], []
			for h in range(Nclump):
				for j in range(Nchiplet):
					if j != i: # This is to make sure there is no duplicate indices which raises an exception.
						for k in range(Nclump):
							fij_index = (i * Nclump * Nchiplet * Nclump * Nmax + h * Nchiplet * Nclump * Nmax + j * Nclump * Nmax + k * Nmax + n) * 2
							row_index.append(fij_index)
							row_coeff.append(1)
							fji_index = (j * Nclump * Nchiplet * Nclump * Nmax + k * Nchiplet * Nclump * Nmax + i * Nclump * Nmax + h * Nmax + n) * 2
							row_index.append(fji_index)
							row_coeff.append(-1)
			problem.linear_constraints.add(lin_expr = [[row_index, row_coeff]], senses = ["E"], rhs = [0])

	# Eq.13 and Eq. 14
	for n in range(Nmax):
		srow_index, srow_coeff = [], []
		trow_index, trow_coeff = [], []
		for h in range(Nclump):
			for j in range(Nchiplet):
				for k in range(Nclump):
					fs_index = (j * Nclump * Nchiplet * Nclump * Nmax + k * Nchiplet * Nclump * Nmax + s[n] * Nclump * Nmax + h * Nmax + n) * 2
					srow_index.append(fs_index)
					srow_coeff.append(1)
					ft_index = (t[n] * Nclump * Nchiplet * Nclump * Nmax + h * Nchiplet * Nclump * Nmax + j * Nclump * Nmax + k * Nmax + n) * 2
					trow_index.append(ft_index)
					trow_coeff.append(1)
		problem.linear_constraints.add(lin_expr = [[srow_index, srow_coeff]], senses = ["E"], rhs = [0])
		problem.linear_constraints.add(lin_expr = [[trow_index, trow_coeff]], senses = ["E"], rhs = [0])

	# Eq.15
	pmax = 300
	for i in range(Nchiplet):
		for h in range(Nclump):
			row_index, row_coeff = [], []
			for j in range(Nchiplet):
				if i != j:
					for k in range(Nclump):
						for n in range(Nmax):
							fij_index = (i * Nclump * Nchiplet * Nclump * Nmax + h * Nchiplet * Nclump * Nmax + j * Nclump * Nmax + k * Nmax + n) * 2
							row_index.append(fij_index)
							row_coeff.append(1)
							fji_index = (j * Nclump * Nchiplet * Nclump * Nmax + k * Nchiplet * Nclump * Nmax + i * Nclump * Nmax + h * Nmax + n) * 2
							row_index.append(fji_index)
							row_coeff.append(1)
			problem.linear_constraints.add(lin_expr = [[row_index, row_coeff]], senses = ["L"], rhs = [pmax])

	# Eq. 16
	for i in range(Nchiplet):
		for h in range(Nclump):
			for j in range(Nchiplet):
				for k in range(Nclump):
					for n in range(Nmax):
						f_index = (i * Nclump * Nchiplet * Nclump * Nmax + h * Nchiplet * Nclump * Nmax + j * Nclump * Nmax + k * Nmax + n) * 2
						# problem.indicator_constraints.add(indvar=f_index+1, rhs = 1.0, sense = "G", lin_expr=[f_index, 1.0], indtype=problem.indicator_constraints.type_.if_)
						problem.indicator_constraints.add(indvar = f_index + 1, rhs = 1.0, sense = "G", lin_expr = [[f_index], [1.0]], indtype = 3)
	print (problem.indicator_constraints.get_num())

	# Eq. 17
	problem.variables.add(lb = [0.0], ub = [100.0], types = [problem.variables.type.integer])
	for i in range(Nchiplet):
		for h in range(Nclump):
			for j in range(Nchiplet):
				for k in range(Nclump):
					for n in range(Nmax):
						f_index = (i * Nclump * Nchiplet * Nclump * Nmax + h * Nchiplet * Nclump * Nmax + j * Nclump * Nmax + k * Nmax + n) * 2 + 1
						problem.linear_constraints.add(lin_expr=[[[f_index, num_val],[-d[i][h][j][k], 1]]], senses = ["G"], rhs = [0.0])

	# Eq. 18
	for n in range(Nmax):
		row_index, row_coeff = [], []
		for i in range(Nchiplet):
			for h in range(Nclump):
				for j in range(Nchiplet):
					for k in range(Nclump):
						f_index = (i * Nclump * Nchiplet * Nclump * Nmax + h * Nchiplet * Nclump * Nmax + j * Nclump * Nmax + k * Nmax + n) * 2
						row_index.append(f_index)
						row_coeff.append(1)
		problem.linear_constraints.add(lin_expr = [[row_index, row_coeff]], senses = ["L"], rhs = [R[s[n]][t[n]]])

	problem.objective.set_linear(num_val, 1.0)
	# print (problem.objective.get_linear())

	problem.solve()	

	for i,x in enumerate(problem.solution.get_values()):
		if x!=0:
			print (i,x)


if __name__ == "__main__":
	solve_Cplex()