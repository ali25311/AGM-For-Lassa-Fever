from itertools import filterfalse
from mesa import Agent, Model
from mesa.time import RandomActivation # random order of agent actions
from mesa.space import MultiGrid # multiple agents per cell
from mesa.datacollection import DataCollector

import random

# A class representing a 'human' agent. Note we're passing in the Agent class
# we imported from the mesa library. Remember that this means our class here
# is inheriting from the 'parent' Agent class, and our class is the 'child', 
# which inherits all the attributes and methods of the parent, but may have some of its own.
class Human_Agent(Agent):
  # Constructor
  def __init__(self, unique_id, model, initial_infection, transmissibility, level_of_movement, mean_length_of_disease, treatment_chance, treatment_length, isolation):
    # Call the constructor from the parent Agent class, which will do all
    # the hard work of defining what an agent is - we just give it an ID
    # and a model that it will live in
    super().__init__(unique_id, model)

    # Now we define the attributes of our Human Agent that aren't in the parent class
    # First, we specify the level of transmissiblity (the probability of passing the disease onto someone else after contact with them
    # assuming this agent is infected, and the other one isn't)
    self.transmissibility = transmissibility

    # The probability that the agent will move from its current location
    # at any given time step
    self.level_of_movement = level_of_movement

    # Average duration of being infected with the disease
    self.mean_length_of_disease = mean_length_of_disease

    # Duration of treatment
    self.length_of_treatment = treatment_length

    self.is_human = True 
    self.infected = False
    self.susceptible = True
    self.exposed = False
    self.removed = False
    self.death = False
    self.treat_length = treatment_length
    self.treat_chance = treatment_chance
    self.iso_chance = isolation
    # potential fix, do not remove:
    self.human_susceptible = self.susceptible
    self.human_infected = self.infected

  # Agent movement function - this is called if it is determined the agent
  # is going to move on this time step
  def move(self):
    # Get a list of possible neighbouring cells to which to move
    # we use the get_neighborhood function, giving it the agent's current
    # position on the grind, stating we want a Moore neighbourhood (which
    # includes diagonals), and that we don't want to include the centre
    # (where the agent is currently) in the returned neighbourhood list
    possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)

    # Select new position at random
    new_position = random.choice(possible_steps)

    # Move the agent tothe randomly selected new position
    self.model.grid.move_agent(self, new_position)
  
  # Step method - this defines which of the agent's actions will be taken
  # on a time step, and in which order
  def step(self):
    # For Isolation length
    if self.removed == True:
      self.treat_length -= 1
      if self.treat_length <= 0:
        self.removed = True
        # self.susceptible = True

    # Move with given probability 
    if (random.uniform(0, 1) < self.level_of_movement) and (self.removed == False):
      self.move()

    # Exposed
    if self.exposed == True:
      self.susceptible = False
      if random.randint(0,100) < self.treat_chance:
        self.exposed = False
        self.susceptible = False
        self.human_susceptible = False
        self.removed = True
      else:
        if random.uniform(0, 1) < self.transmissibility:
          self.exposed = False
          self.infected = True
          self.human_infected = True
          self.susceptible = False
          self.human_susceptible = False
          self.removed = False
          self.disease_duration = int(round(random.expovariate(1.0 / self.mean_length_of_disease), 0))
        else:
          self.exposed = False
          self.susceptible = True
          self.human_susceptible = True
          
      if random.randint(0,100) < self.treat_chance:
        self.exposed = False
        self.susceptible = False
        self.human_susceptible = False
        self.removed = True
    
    # Begin infecting cellmates (if agent is infected), and update
    # remaining disease duration
    if self.infected == True:
      # self.infect()
      # decrement remaining disease duration by one time unit
      self.disease_duration -= 1

      # if disease has now run its course, flag that the agent is no
      # longer infected
      if self.disease_duration <= 0:
        self.infected = False
        self.human_infected = False
        self.susceptible = False
        self.human_susceptible = False
        self.removed = True
  
# ===================================
# rodents class
class Rodent_Agent(Agent):
  # Constructor
  def __init__(self, unique_id, model, initial_infection, transmissibility, level_of_movement, mean_length_of_disease, environmental, pesticide):
    # Call the constructor from the parent Agent class, which will do all
    # the hard work of defining what an agent is - we just give it an ID
    # and a model that it will live in
    super().__init__(unique_id, model)
    
    # Now we define the attributes of our Rodent Agent that aren't in the parent class
    # First, we specify the level of transmissiblity (the probability of passing the disease onto someone else after contact with them
    # assuming this agent is infected, and the other one isn't)
    self.transmissibility = transmissibility

    # The probability that the agent will move from its current location
    # at any given time step
    self.level_of_movement = level_of_movement

    # Average duration of being infected with the disease
    self.mean_length_of_disease = mean_length_of_disease

    self.is_human = False 
    self.death = False
    self.pesticide_level = pesticide
    self.environmental_level = environmental
    self.exposed = False
    self.removed = False
    # test, dont remove
    self.human_susceptible = False
    self.human_infected = False

    # We're going to set up our model so that some agents are already
    # infected at the start. We've got a paramter value passed in
    # (initial infection) that defines the probability of any given agent 
    # being infected at the start. So, we just randomly sample from 
    # uniform distribution between 0 and 1, and if the sampled value is
    # less than this probability, then we say that the agent is infected -
    # we set their Boolean infected attribute to True, and randomly
    # sample a duration we passed in. Otherwise, we set their infected attribute to false
    if random.uniform(0, 1) < initial_infection:
      self.infected = True
      self.susceptible = False
      self.disease_duration = int(round(random.expovariate(1.0 / self.mean_length_of_disease), 0))
    else:
      self.infected = False
      self.susceptible = True

  # @41:36 ✔️
  # Agent movement function - this is called if it is determined the agent
  # is going to move on this time step
  def move(self):
    # Get a list of possible neighbouring cells to which to move
    # we use the get_neighborhood function, giving it the agent's current
    # position on the grind, stating we want a Moore neighbourhood (which
    # includes diagonals), and that we don't want to include the centre
    # (where the agent is currently) in the returned neighbourhood list
    possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)

    # Select new position at random
    new_position = random.choice(possible_steps)

    # Move the agent to the randomly selected new position
    self.model.grid.move_agent(self, new_position)

  # Agent infection function
  def infect(self):
    # Get list of agents in this cell. We use the get_cell_list_contents
    # function of the grid object and pass it our current position
    cellmates = self.model.grid.get_cell_list_contents([self.pos])

    # Check if there are other agents here - if the list of cellmates is 
    # greater than 1 then there must be more here than this agent
    if len(cellmates) > 1:
      # for each agent in the cell
      for inhabitant in cellmates:
        # infect the agent with a given probability (transmissibility)
        # if they're not already infected. If they become infected,
        # then we set their infected attribute to True, and their
        # disease_duration attribute to a value randomly sampled based
        # on the mean_length_of_distance attribute.
        if inhabitant.infected == False and inhabitant.is_human:
          if self.infected == True:
            inhabitant.exposed = True
            inhabitant.susceptible = False
            inhabitant.human_susceptible = False
        elif inhabitant.exposed == True:
          if self.infected == True:
            inhabitant.infected == True
            inhabitant.human_infected = True
            inhabitant.exposed = False
            inhabitant.susceptible = False
            inhabitant.human_susceptible = False

  def pesticideFactor(self):
    if random.randint(0,100) < self.pesticide_level:
      self.death = True
      self.infected = False
      self.susceptible = False
    
  # Step method - this defines which of the agent's actions will be taken
  # on a time step, and in which order
  def step(self):
    # Pesticide function that will determine if a rodent will die or not
    self.pesticideFactor()
    if self.death == True:
      return
    # Environmental if loop that will determine if a rodent will move or not
    if random.randint(0,100) < self.environmental_level:
      return
    else:
      # Move with given probability 
      if random.uniform(0, 1) < self.level_of_movement:
        self.move()

    self.exposed = False
    # Begin infecting cellmates (if agent is infected), and update
    # remaining disease duration
    if self.infected == True:
      self.infect()
      # decrement remaining disease duration by one time unit
      self.disease_duration -= 1

      # if disease has now run its course, flag that the agent is no
      # longer infected
      if self.disease_duration <= 0:
        self.infected = False
        self.susceptible = True


class Disease_Model(Model):
  # 2D Model initialisation function - initialise with N agents, and
  # specified width and height. Also pass in the things we need to pass
  # to our agents when instantiating them.
  # The comment below which uses triple " will get picked up by the server
  # if we run a live display of the model.
  """A model of how Lassa Fever spreads and how different interventions effect the overall virus spread and reproduction rate. KEY: Circles = Humans, Squares = Rodents"""
  def __init__(self, N, width, height, initial_infection, transmissibility, level_of_movement, mean_length_of_disease, rodent_population, treatment_chance, treatment_length, isolation, environmental, pesticide):
    self.running = True # required for BatchRunner
    self.num_humans = N # assign number of humans at initialisation
    self.num_rodents = rodent_population # assign number of rodents at initialisation
    agent_id_count = 0 # for assigning each agent (both rodent & human) with their own unique ID number

    # Set up Toroidal multi-grid (Toroidal = if the agent is in a cell
    # on the border of the grid, and moves towards the border, they'll
    # come out the other side. Think PacMan :) The True Boolean passed in
    # switches that on. Multi-grid just means we can have more than one
    # agent per cell)
    self.grid = MultiGrid(width, height, True)
    # set up a scheduler with random order of agents being activated
    # each turn. Remember order is important here - if an infected agent
    # is going to move into a cell with an uninfected agent, but that
    # uninfected agent moves first, they'll escape infection.
    self.schedule = RandomActivation(self)

    # Create human_agent objects up to number specified
    for i in range(self.num_humans):
      # Create agent with ID taken from for loop
      a = Human_Agent(i, self, initial_infection, transmissibility, level_of_movement, mean_length_of_disease, treatment_chance, treatment_length, isolation)
      self.schedule.add(a) # add agent to the schedule
      # Try adding the agent to a random empty cell
      try:
        start_cell = self.grid.find_empty()
        self.grid.place_agent(a, start_cell)
      # If you can't find an empty cell, just pick any cell at randomS
      except:
        x = random.randrange(self.grid.width)
        y = random.randrange(self.grid.height)
        self.grid.place_agent(a, (x,y))
      agent_id_count += 1

    # Create rodent_agent objects up to number specified
    for i in range(self.num_rodents):
      # Create agent with ID taken from for loop
      a = Rodent_Agent(i + agent_id_count, self, initial_infection, transmissibility, level_of_movement, mean_length_of_disease, environmental, pesticide)
      self.schedule.add(a) # add agent to the schedule
      # Try adding the agent to a random empty cell
      try:
        start_cell = self.grid.find_empty()
        self.grid.place_agent(a, start_cell)
      # If you can't find an empty cell, just pick any cell at randomS
      except:
        x = random.randrange(self.grid.width)
        y = random.randrange(self.grid.height)
        self.grid.place_agent(a, (x,y))
        
    # Create a new datacollector, and pass in a model reporter as a
    # dictionary entry, with the index value as the name of the result
    # (which we'll refer to by this name elsewhere) and the lookup value
    # as the name of the function we created below that will calculate
    # the result we're reporting
    self.datacollector = DataCollector(
      model_reporters={"Infected Humans":calculate_number_infected,
                       "Susceptible Humans":calculate_number_susceptible,
                       "Deceased Rodents":calculate_number_deceased,
                       "Exposed Humans":calculate_number_exposed,
                       "Removed/Recovered/Isolated Humans":calculate_number_removed},
      agent_reporters={}
      )

  # Function to advance the mode by one step
  def step(self):
    self.schedule.step()
    # Tell the datacollector to collect data from the specified model
    # and agent reporters
    self.datacollector.collect(self)

# Function to calculate total number infected in the model
# The function takes as an input model object for which we want to calculate
# these results
def calculate_number_infected(model):
  # set up a counter with default value of 0 that wil keep count of the
  # total number infected
  total_infected = 0

  # use list comprehnsion to establish a new list that contains the
  # infected variable value of each agent in the model
  infection_report = [agent.human_infected for agent in model.schedule.agents]

  # loop through the stored variable values which indicate whether each
  # agent is infected, and for each one that is True increment the total
  # number of infected by 1
  for x in infection_report:
    if x == True:
      total_infected += 1

  # Return the total number of infected as the output from the function
  return total_infected

# Function to calculate total number susceptible in the model
def calculate_number_susceptible(model):
  total_susceptible = 0

  susceptible_report = [agent.human_susceptible for agent in model.schedule.agents]

  for x in susceptible_report:
    if x == True:
      total_susceptible  += 1
  
  return total_susceptible

#Function to calculate total number of deceased rodents in the model
def calculate_number_deceased(model):
  total_deceased = 0

  deceased_report = [agent.death for agent in model.schedule.agents]

  for x in deceased_report:
    if x == True:
      total_deceased  += 1
  
  return total_deceased

def calculate_number_exposed(model):
  total_exposed = 0

  exposed_report = [agent.exposed for agent in model.schedule.agents]

  for x in exposed_report:
    if x == True:
      total_exposed += 1
  
  return total_exposed

def calculate_number_removed(model):
  total_removed = 0

  removed_report = [agent.removed for agent in model.schedule.agents]

  for x in removed_report:
    if x == True:
      total_removed += 1
  
  return total_removed
  