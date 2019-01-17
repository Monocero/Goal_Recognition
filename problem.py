###This file is used to construct problem instances in PDDL

def c(i,j):
	#auxiliary function
	return 'c'+str(i)+'-'+str(j)


#Following methods are splitted for code-clarity reasons

def start(i, j):
	return '(at '+c(i,j)+')'
	


def goals(grid):
	goals = []
	n = len(grid)
	m = len(grid[0])
	for i in range(n):
		for j in range(m):
			if grid[i][j] == 2:
				goals.append('(at '+c(i,j)+')')
	return goals


def objects(grid):
	'return objects of problem.pddl; such objects are non-obstacle cells'
	objects = []
	n = len(grid)
	m = len(grid[0])
	for i in range(n):
		for j in range(m):
			if grid[i][j] != 3:
				objects.append(c(i,j))
	return objects
	

#objects and adjacency are called only one time for each running
def adjacency(grid):
	'''Funcion used to define adjacency relations among cells in the user-defined grid
	Since this relations are static, function is invoked only one time, when the grid is constructed'''
	adj_list = [] #list of strings like (adj c11 c12)
	n = len(grid)
	m = len(grid[0])
	for i in range(n):
		for j in range(m):
			if grid[i][j] != 3: #if cell is not an obstacle
				
				if i>0 and j>0: #key 1
					if grid[i-1][j-1] !=3:
						adj = '(adj '+c(i,j)+' '+c(i-1,j-1)+')'
						adj_list.append(adj)

				if i>0: #2
					if grid[i-1][j] !=3:
						adj = '(adj '+c(i,j)+' '+c(i-1,j)+')'
						adj_list.append(adj)

				if i>0 and j<m-1: #3 
					if grid[i-1][j+1] !=3:
						adj = '(adj '+c(i,j)+' '+c(i-1,j+1)+')'
						adj_list.append(adj)

				if j>0: #4
					if grid[i][j-1] !=3:
						adj = '(adj '+c(i,j)+' '+c(i,j-1)+')'
						adj_list.append(adj)

				if j<m-1: #6
					if grid[i][j+1] !=3:
						adj = '(adj '+c(i,j)+' '+c(i,j+1)+')'
						adj_list.append(adj)

				if i<n-1 and j>0: #7
					if grid[i+1][j-1] !=3:
						adj = '(adj '+c(i,j)+' '+c(i+1,j-1)+')'
						adj_list.append(adj)

				if i<n-1: #8
					if grid[i+1][j] !=3:
						adj = '(adj '+c(i,j)+' '+c(i+1,j)+')'
						adj_list.append(adj)

				if i<n-1 and j<m-1: #9
					if grid[i+1][j+1] !=3:
						adj = '(adj '+c(i,j)+' '+c(i+1,j+1)+')'
						adj_list.append(adj)

	return adj_list


def problem_template(object_list, adj_list):
	#construct problem.pddl
	problem = open("problem_template.pddl","w+")
	heading = '(define (problem grid_prob) \r(:domain grid) \r(:objects \r'
	problem.write(heading)
	for obj in object_list:
		problem.write(obj)
		problem.write(' ')
	problem.write('\r)')
	init = '\r(:init \r'
	problem.write(init)
	for adj in adj_list:	
		problem.write(adj)
		problem.write('\r')
	problem.write('START_PLACEHOLDER')
	problem.write('\r)')
	goal_string = '\r(:goal \r'
	problem.write(goal_string)
	problem.write('GOAL_PLACEHOLDER')
	problem.write('\r)')
	problem.write('\r)')
	problem.close()

def problem(start, goal):
	# Read in the file
	problem_file = open("problem_template.pddl",'r')
	problem_data = problem_file.read()
	problem_file.close()
	# Replace the target string
	problem_data = problem_data.replace('START_PLACEHOLDER', start)
	problem_data = problem_data.replace('GOAL_PLACEHOLDER', goal)
	# Write the file out again
	problem_file = open("problem.pddl",'w+')
	problem_file.write(problem_data)
	problem_file.close()
