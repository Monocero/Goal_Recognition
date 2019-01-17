import pygame
import sys
import os
from problem import *
from probability import *

#Reading grid dimensions passed from terminal. Only dimensions in [5,25] are accepted. If some error occurs default dimensions are used
if len(sys.argv) == 3 and sys.argv[1].isdigit() and sys.argv[2].isdigit(): 
	n, m = sys.argv[1:]
	n = int(n)  #num of rows
	if n<5:
		n=5
	elif n>25:
		n= 25
	m = int(m)  #num of columns
	if m<5:
		m=5
	elif m>25:
		m = 25
else: 
	n = 11
	m = 11

os.system('rm -f plots/*') #remove previous plots



side = 35 #side of the square 

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
 
# This sets the WIDTH and HEIGHT of each grid cell
WIDTH = side
HEIGHT = side
 
# This sets the margin between each cell
MARGIN = 5


# Legend
# 0 = regular cell
# 1 = initial cell
# 2 = goal cell
# 3 = obstacle
grid = [[0 for j in range(m)] for i in range(n)]




# Initialize pygame
pygame.init()


 
# Set the HEIGHT and WIDTH of the screen
SCREEN_WIDTH = (MARGIN + WIDTH) * m + MARGIN
SCREEN_HEIGHT = (MARGIN + HEIGHT) * n + MARGIN

WINDOW_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode(WINDOW_SIZE)
 
 
# Used to manage how fast the screen updates
#clock = pygame.time.Clock()



def legal_position(i,j):
	# Determine if (i,j) is a legal cell for the actor to be in 
	if i<0 or i>=n or j<0 or j>=m: return False #(i, j) does not represent a cell
	elif grid[i][j] == 3: return False #in the cell there is an obstacle
	return True

def draw_grid():
	for i in range(n):
		for j in range(m):
			if grid[i][j] == 1:
				color = GREEN
			elif grid[i][j] == 2:
				color = RED
			elif grid[i][j] == 3:
				color = BLACK
			else:
				color = WHITE
			i_, j_ =  j, n-1 - i #'graphics to matrix-like' numbering  (with rows increasing bottom up)
			pygame.draw.rect(screen,
                             color,
                             [(MARGIN + WIDTH) * i_ + MARGIN,
                              (MARGIN + HEIGHT) * j_ + MARGIN,
                              WIDTH,
                              HEIGHT])


pygame.display.set_caption("Probabilistic Goal Recognition - Grid World")



# --------- Fill Grid ----------

def caption():
	if v == 1:
		pygame.display.set_caption("Select Initial Cell")
	elif v == 2:
		pygame.display.set_caption("Select Goal Cells - Press Enter When Finished")
	elif v == 3:
		pygame.display.set_caption("Select Obstacle Cells - Press Enter When Finished")
	else:
		pygame.display.set_caption("Probabilistic Goal Recognition - Grid World")



v = 1 #value assigned to a cell when clicking, according to the legend
while True:
	# Draw the grid
	draw_grid()
	caption()
	pygame.display.flip()
	if v == 4:
		break
	for event in pygame.event.get():  # User did something
		if event.type == pygame.QUIT:  # If user clicked close
			pygame.quit()
		elif event.type == pygame.MOUSEBUTTONDOWN:
			# User clicks the mouse. Get the position
			pos = pygame.mouse.get_pos()
			# Change the x/y screen coordinates to graphic numbering
			j = pos[0] // (WIDTH + MARGIN)
			i = pos[1] // (HEIGHT + MARGIN)
			# change coordinates
			j, i =  j, n-1 - i
			# Set that cell to the desired type if not yet used as special cell
			if grid[i][j]==0:
				grid[i][j] = v
			if v==1:
				# Actor position
				actor_position_i = i
				actor_position_j = j
				v +=1
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_RETURN:
				v += 1


# ----------- PDDL -------------

object_list = objects(grid) #return objects of problem.pddl; such objects are non-obstacle cells
adj_list = adjacency(grid) #used to construct problem.pddl
problem_template(object_list, adj_list) #create problem.pddl with placeholders instead of start and goal position

goal_list = goals(grid) #list of all goals
init = start(actor_position_i, actor_position_j)


#Compute the cost of reaching goal starting from initial position 
original_cost_goal = [] #original costs to reach the goals; they'll be compared with costs from new positions
for goal in goal_list:
	cost = compute_cost(init, goal) #create problem.pddl file, run FD and return solution cost
	original_cost_goal.append(cost)


# -------- Main Program Loop -----------
num_act = 0 #number executed actions
original_goal_probability = [1/len(goal_list) for goal in goal_list] #initialize probabilities uniformly 
print(original_goal_probability)
plot_probabilities(original_goal_probability, num_act)


done = False
while not done:
	
	for event in pygame.event.get():  # User did something
		if event.type == pygame.QUIT:  # If user clicked close
			done = True
		elif event.type == pygame.KEYDOWN: 
			i = actor_position_i
			j = actor_position_j
			if event.key == pygame.K_KP1:
				i -= 1
				j -= 1
				if legal_position(i,j):
					actor_position_i = i
					actor_position_j = j
					num_act +=1 
					goal_probability = update_probabilities(start(actor_position_i, actor_position_j), num_act, original_cost_goal, goal_list, original_goal_probability) #it does not depend from the particular action, just the state resulting from the action, but it must be putted here and repeated to be trigged only when a relevant key is pressed
			elif event.key == pygame.K_KP2:
				i -= 1
				if legal_position(i,j):
					actor_position_i = i
					num_act +=1 
					goal_probability = update_probabilities(start(actor_position_i, actor_position_j), num_act, original_cost_goal, goal_list, original_goal_probability)
			elif event.key == pygame.K_KP3:
				i -= 1
				j += 1
				if legal_position(i,j):
					actor_position_i = i
					actor_position_j = j
					num_act +=1 
					goal_probability = update_probabilities(start(actor_position_i, actor_position_j), num_act, original_cost_goal, goal_list, original_goal_probability)
			elif event.key == pygame.K_KP4:
				j -= 1
				if legal_position(i,j):
					actor_position_j = j
					num_act +=1 
					goal_probability = update_probabilities(start(actor_position_i, actor_position_j), num_act, original_cost_goal, goal_list, original_goal_probability)
			elif event.key == pygame.K_KP6:
				j += 1				
				if legal_position(i,j):
					actor_position_j = j
					num_act +=1 
					goal_probability = update_probabilities(start(actor_position_i, actor_position_j), num_act, original_cost_goal, goal_list, original_goal_probability)
			elif event.key == pygame.K_KP7:
				i += 1
				j -= 1
				if legal_position(i,j):
					actor_position_i = i
					actor_position_j = j
					num_act +=1 
					goal_probability = update_probabilities(start(actor_position_i, actor_position_j), num_act, original_cost_goal, goal_list, original_goal_probability)
			elif event.key == pygame.K_KP8:
				i += 1
				if legal_position(i,j):
					actor_position_i = i
					num_act +=1 
					goal_probability = update_probabilities(start(actor_position_i, actor_position_j), num_act, original_cost_goal, goal_list, original_goal_probability)		
			elif event.key == pygame.K_KP9:
				i += 1
				j += 1
				if legal_position(i,j):
					actor_position_i = i
					actor_position_j = j 
					num_act +=1 
					goal_probability = update_probabilities(start(actor_position_i, actor_position_j), num_act, original_cost_goal, goal_list, original_goal_probability)
			print(goal_probability)
			plot_probabilities(goal_probability, num_act)
	# Set the screen background
	screen.fill(BLACK)

	# Draw the grid
	draw_grid()
 
	# Draw actor position
	actor_position_i_ = actor_position_j
	actor_position_j_ = n-1- actor_position_i
	actor = pygame.image.load('actor.png')
	actor = pygame.transform.scale(actor, (WIDTH, HEIGHT))
	x = (MARGIN + WIDTH) * actor_position_i_ + MARGIN
	y = (MARGIN + HEIGHT) * actor_position_j_ + MARGIN
	screen.blit(actor, (x, y))

	
	# Limit to 60 frames per second
	#clock.tick(60)
 
	# Go ahead and update the screen with what we've drawn.	
	pygame.display.flip()

# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit()
 
