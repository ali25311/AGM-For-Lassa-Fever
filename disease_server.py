# We'll first import from the module that we ourselves created! We only need
# the Disease_Model class bit of the module here so that's all we'll import
from disease_model import Disease_Model
# This will import the type of grid we want to visualise our agents
from mesa.visualization.modules import CanvasGrid
# This will import the ModularServer class, which allows us to create a new 
# server to host the visualisation of our model
from mesa.visualization.ModularVisualization import ModularServer
# This will import to ModularServer class, which allows us to create a new
# server to host the visualisation of our model
from mesa.visualization.UserParam import UserSettableParameter
# (below) Lastly, we add the ChartModule(used for drawing graphs)
from mesa.visualization.modules import ChartModule

# Portrayal function that defines how agents will be drawn onto the grid
# We specify that the function takes an agent as its input - it wil draw the
# agent passed to it in the manner we define in this function
def agent_portrayal(agent):

  # Specify visual characteristics for each human agents status (infected, removed, susceptible, etc.)
  # Here, we specifiy that if an agent is infected/removed/etc..., then colour them that specific color, and put them on their respective layer
  # We put agents on different levels so they'll appear on top of infected agents if multiple agents occupy the same cell

  # IF agent is a human
  if agent.is_human == True:
    
    # Set up portrayal dictionary to store the key aspects of our portrayal
    portrayal = {"Shape":"circle", "Filled":"true", "r":0.6}
    if agent.infected == True:
      # Infected
      portrayal["Color"] = "red"
      portrayal["Layer"] = 0

    elif agent.exposed == True:
      portrayal["Color"] = "lime"
      portrayal["r"] = 0.55
      portrayal["Layer"] = 0.6

    elif agent.susceptible == True:
      # Susceptible
      portrayal["Color"] = "orange"
      portrayal["r"] = 0.2
      portrayal["Layer"] = 0.1

    elif agent.removed == True:
      portrayal["Color"] = "blue"
      portrayal["r"] = 0.3
      portrayal["Layer"] = 0.1

  # IF agent is a rodent
  else:
    portrayal = {"Shape":"rect", "Filled":"false", "w":0.5, "h":0.5}
    if agent.infected == True:
      # Infected
      portrayal["Color"] = "red"
      portrayal["Layer"] = 0.3

    elif agent.susceptible == True:
      # Susceptible
      portrayal["Color"] = "orange"
      portrayal["w"] = 0.2
      portrayal["h"] = 0.2
      portrayal["Layer"] = 0.4

    elif agent.death == True:
      portrayal["Color"] = "gray"
      portrayal["w"] = 0.1
      portrayal["h"] = 0.1
      portrayal["Layer"] = 0
  return portrayal


# Set up visualisation elements
# Set up a CanvasGrid, that portrays agents as defined by the portrayal
# (small grid), make sure to change width and length on line 128 as well to 10x10 if using small grid and vice versa
# grid = CanvasGrid(agent_portrayal,10,10,500,500)
# For this instance, we will use a large grid
# function we defined, has 20 x 20 cells, and a display size of 700x700 pixels
grid = CanvasGrid(agent_portrayal,20,20,700,700)


# Set up a chart to represent the totals of each population over time. We instantiate a 
# ChartModule for this, and pass in a dictionary containing the label for the
total_graph = ChartModule(
  [{"Label":"Infected Humans", "Color":"Red"},
   {"Label":"Susceptible Humans", "Color":"Orange"},
   {"Label":"Deceased Rodents", "Color":"Gray"},
   {"Label":"Exposed Humans", "Color":"Lime"},
   {"Label":"Removed/Recovered/Isolated Humans", "Color":"Blue"}],
  data_collector_name='datacollector'
  )

# Set up user sliders. For each, we create an instance of the 
# UserSettableParameter class, and pass to it that we want a slider, the
# slider, and the increments of change for the slider.
# (default value, minmum value, max value, increment)
number_of_agents_slider = UserSettableParameter('slider',"Number of Humans", 200, 2, 200, 1)
initial_infection_slider = UserSettableParameter('slider', "Probability of Rodent Initial Infection", 0.9, 0.01, 1, 0.01)
transmissibility_slider = UserSettableParameter('slider', "Transmissibility (Only Rodents)", 1, 0.01, 1, 0.01)
level_of_movement_slider = UserSettableParameter('slider', "Level of Movement (humans & rodents)", 0.56, 0.01, 1, 0.01)
mean_length_of_disease_slider = UserSettableParameter('slider', "Mean Length of Disease days", 18, 1, 100, 1)
# new sliders
rodent_population_slider = UserSettableParameter('slider', "Number of Rodents", 200, 1, 200, 1)
treatment_chance_slider = UserSettableParameter('slider', "Chance of Treatment", 35, 1, 100, 1)
treatment_length_slider = UserSettableParameter('slider', "Length of Treatment/Isolation In Days", 40, 1, 100, 1)
isolation_slider = UserSettableParameter('slider', "Chance of Exposed Human Being Placed in Isolation", 60, 1, 100, 1)
environmental_slider = UserSettableParameter('slider', "Environmental Control (Rodents Chance of Not Moving)", 0, 0, 50, 1)
pesticide_slider = UserSettableParameter('slider', "Pesticide Control (Rodents Chance of Dying)", 0, 0, 50, 1)


# Set up the server as a ModularServer, passing in the model class we
# imported earlier, the list of elements we want to visualise (just the grid
# here), the title to display for the server visualisation, and each user
# interface we want to incluide (our  sliders here) in a dictionary, where the
# index name in " marks must match the respective variable name in the Model
# class, and the lookup value is the name of the slider we declared above
# (ie "name_of_variable":name_of_slider)
server = ModularServer(Disease_Model, [grid, total_graph],  "Lassa Fever Spread Model",
                      {"N":number_of_agents_slider, "width":20, "height":20,
                       "initial_infection":initial_infection_slider,
                       "transmissibility":transmissibility_slider,
                       "level_of_movement":level_of_movement_slider,
                       "mean_length_of_disease":mean_length_of_disease_slider,
                       "rodent_population":rodent_population_slider,
                       "treatment_chance":treatment_chance_slider,
                       "treatment_length":treatment_length_slider,
                       "isolation":isolation_slider,
                       "environmental":environmental_slider,
                       "pesticide":pesticide_slider
                       }
                      )

