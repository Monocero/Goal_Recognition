from problem import problem 
import os
from math import exp
import matplotlib.pyplot as plt


BETA = 0.5 #parameter governing Boltzmann distribution

def compute_cost(start, goal):
	#create problem.pddl file, run FD and return solution cost
	problem(start, goal)
	os.system(' ./downward/fast-downward.py domain.pddl problem.pddl --search "astar(lmcut())" > /dev/null')
	if os.path.isfile('sas_plan'):
		solution = open('sas_plan', 'r')
		last_line = solution.readlines()[-1].split()
		cost = int(last_line[3])
		solution.close()
	else: cost = 'inf' #if does not exists a solution
	return cost 
	
def	update_probabilities(start, num_act, original_cost_list, goal_list, goal_probability):
	'''params:
		start: current position (right after executing action)
		num_act: number actions executed
		goal_list: list of all possible goals
		goal_probability: probability of the corresponding goal
		original_cost_list: cost of reaching corresponding goal from original starting position'''
	n = len(goal_list)
	likelihoods = []
	for index in range(n):
		cost = compute_cost(start, goal_list[index])
		if cost != 'inf':
			delta = (cost + num_act) - original_cost_list[index]
		else: delta = 100000
		prObs = exp(-BETA*delta)/(1+exp(-BETA*delta))
		likelihoods.append(prObs)
	scores = [likelihoods[i]*goal_probability[i] for i in range(n)]
	new_probability = [score/sum(scores) for score in scores]
	return new_probability
	

def plot_probabilities(goal_probability, num):
	plt.xticks([])
	plt.ylim(0,1)
	plt.bar(range(len(goal_probability)), goal_probability)
	plt.savefig('plots/action'+str(num))
	plt.gcf().clear() #to clean plot and avoid plotting previous bars on the same plot
	

		
	

		

	
	 
	

