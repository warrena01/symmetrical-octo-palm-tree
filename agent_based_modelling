'''
1. Define a Schelling Class
    6. Define a list of relative neighbours using list comprehension
    Initialise and populate the model
        2. Construct the class and instance variables (width, height, empty ratio, similarity ratio, n iterations)
        3. Create a list of houses for each cell using h x w as a grid and randomising the order
        4. Define number of empty houses
        5. Using list slicing and comprehension, assign empty, red, and blue houses
    Test House Satisfaction
        6. Loop through all cells and check if they are satisfied with their neighbours
        7. Assess counters to hceck if the overall satisfaction level matches input
    Run the model
        8. Loop through each cell and if its unhappy, move it and update the model within a range
        9. Update to show that a change was made (if there was an unhappy cell)
        10. Exit if n_changes = 0 as optimal solution has been found
        11. Update user if the range was met and no optimal solution was found


'''

from random import shuffle, choice, seed
import matplotlib.pyplot as plt
from copy import deepcopy


# define our class mdoel (the mechanics of the model)
class Schelling:

    # class variable containing list of neighbours
    neighbours = [ (i, j) for i in range(-1, 2) for j in range(-1, 2) if (i, j) != (0, 0) ]

    # construct our class
    def __init__(self, width, height, empty_ratio, similarity_threshold, n_iterations):
        '''
        *** INITIALISE AND POPULATE THE MODEL (SET UP THE CLASS)
        width/height = size of area
        empty_ratio = number of empty cells permitted as a ration
        similarity_threshold = tolerance allowed by the agents
        n_iterations = # of iterations where agents are allowed to move
        '''
        # create our starting instance variables
        self.width = width
        self.height = height
        self.empty_ratio = empty_ratio
        self.similarity_threshold = similarity_threshold
        self.n_iterations = n_iterations 
        self.agents = {} # initialise an agent module that describes what an agent can do/know

        # get all the house addresses and randomise the order
        all_houses = [(x,y) for x in range(self.width) for y in range(self.height)]
        shuffle(all_houses)
        n_empty = int( self.empty_ratio * len(all_houses) ) # define how many empty houses there should be based on ratio
        self.empty_houses = all_houses[:n_empty] # assign first n houses up until len(n_empty) as empty houses
        
        remaining_houses = all_houses[n_empty:] # assign the houses that arent empty
        red_group = [[coords, 'red'] for coords in remaining_houses[0::2]] # all even numbers
        blue_group = [[coords, 'blue'] for coords in remaining_houses[1::2]] # all odd numbers
        self.agents.update(dict(red_group + blue_group)) # add both sets of agents to the instance variable
        

    def is_unsatisfied(self, agent):
        '''
        *** THIS TESTS THE LEVEL OF SATISFACTION FOR EACH STATE OF THE MODEL
        '''
        count_similar = 0 # initialise variable, keep track of # of neighbours in same/diff group
        count_different = 0 # initialise variable, keep track of # of neighbours in same/diff group

        for n in self.neighbours: # loop through the neighbours to update the satisfaction
            try:
                #               add two coordinates to make the relative position
                if self.agents[(agent[0]+n[0], agent[1]+n[1])] == self.agents[agent]:
                    count_similar += 1
                else:
                    count_different += 1
            except KeyError: # if we go off the map or it is an empty house
                continue
        try: # return whether or not the proportion of similar neighbours is acceptable
            return count_similar / (count_similar + count_different) < self.similarity_threshold
        except ZeroDivisionError:
            return False
        

    def run_model(self):
        '''
        *** RUN THE MODEL
        '''
        for i in range(1, self.n_iterations+1): # run through for n_iterations times
            self.old_agents = deepcopy(self.agents) # create a copy of the agents
            n_changes = 0 # initialise a variable to count the number of changes
            for agent in self.old_agents: # loop through each house.
                if self.is_unsatisfied(agent) == True: # move those that are unsatisfied
                    empty_house = choice(self.empty_houses) # randomly choose a new location
                    self.agents[empty_house] = self.agents[agent] # update dictionary
                    del self.agents[agent] # delete from the dictionary
                    self.empty_houses.append(agent) # add new empty space left behind
                    self.empty_houses.remove(empty_house) # remove the space taken
                    n_changes += 1 # update the number of changes.

            print(f"Iteration: {i}, Number of changes: {n_changes}") # update the user on changes

            # stop iterating if no changes happened
            if n_changes == 0:
                print(f"\nFound optimal solution at {i+1} iterations\n")
                break
        # if we did not find an optimal solution
        if (i == self.n_iterations) == True:
            print(f"\nOptimal solution not found after {self.n_iterations} iterations\n")
		
        return i # return the number of iterations
                    

    def plot(self, my_ax, title):
        '''
        *** THIS CAN BE CALLED ON TO PLOT THE STATE MODEL AT THE TIME AT WHICH IS IT CALLED
        '''       
        my_ax.set_title(title, fontsize = 10, fontweight = 'bold')
        my_ax.set_xlim([0, self.width])
        my_ax.set_ylim([0, self.height])
        my_ax.set_xticks([])
        my_ax.set_yticks([])

        for agent in self.agents:
            my_ax.scatter(agent[0]+0.5, agent[1]+0.5, color=self.agents[agent])


''' CREATING DATA AND PLOTTING'''

seed(1824)

schelling = Schelling(25, 25, 0.25, 0.6, 500) # create our object and define its class with the necessary parameters/information

# create axis object and plopt at the first point of model population
fig, my_axs = plt.subplots(nrows=1, ncols=2, figsize=(14,6))
plt.subplots_adjust(wspace=0.1)

schelling.plot(my_axs[0], 'Initial State') # plot the initial state (as we havent called anything else for the class to do yet)

# start the movement of the agents and plot this map
iterations = schelling.run_model()
schelling.plot(my_axs[1], 'Final State')

# add the overall title into the model
fig.suptitle(f"Schelling Model of Segregation ({schelling.similarity_threshold * 100:.2f}% Satisfaction after {iterations} iterations)")
print('done')
plt.show()
