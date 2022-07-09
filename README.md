# Lassa Fever Agent-Based Model
**Model developed by Ali Hussain, as part of Undergraduate Research into environmental modeling Lassa Fever.**

### What is Lassa Fever?
Lassa Fever (LF) is an acute zoonotic viral hemorrhagic illness. The causative agent is the Lassa virus, hosted by a species of rodent called Mastomys natalensis. It spreads to humans through contact with food or household items that have been contaminated with rodent feces or from an infected person to another. LF is endemic in most countries of West Africa, and may spread to other parts of the world, if not checked, according to the Center for Diseases Control and Prevention.

### What's the model for?

This model uses agent-based simulations to evaluate how changing intervention parameters will affect the reproduction 
number or infection rate of an outbreak of Lassa Fever. Some scenarios include situations like increased rodent control, increase isolation, etc. 
**The main objective of the model is to investigate the
effectiveness and sustainability of different strategies for curtailing
the outbreak.**

### How does it work?
The models were implemented
using Mesa, a python-based modelling package.
 For the model development, the population of the study area was
divided into seven groups. Two of the groups; susceptible rodents
(𝑆𝐶𝑟) and infected rodents (𝐼𝐹𝑟 ) were used to simulate rodent
control strategies. The five human sub-groups: susceptible humans
(𝑆𝐶ℎ), infected humans (𝐼𝐹ℎ), isolated humans (𝐼𝑆ℎ), treated
humans (𝑇𝑅ℎ), recovered (𝑅𝐶ℎ) and removed humans (𝑅𝑉ℎ)
represent agent groups of the population. 𝜇𝑟 , 𝜇𝑟ℎ, and 𝜇ℎ represent
the forces of infection from susceptible rodents to infected rodents;
from this group to infected humans, and from susceptible humans
to infected sub-group respectively. Agents within the human population become infected either
through contacts with infected rodents or from exposed humans.
The rate at which infected individuals become isolated is
represented by 𝛽ℎ . The treatment availability is controlled by a rate,
𝜌ℎ. Individuals in the treated group may either move to the
recovered group (using a rate of 𝛼ℎ) or removed (dead) group,
using by a rate of 𝛿1ℎ.

![model structure](https://i.imgur.com/OOvsATF.png)

### How does it look?
![model structure](https://i.imgur.com/QMrsQ5O.png)
+ The circles represent human agents, while the squares represent rodent agents.
+ *COLOR CODE For Rat Agents:* Yellow = Susceptible | Red = Infected | Gray = Deceased
+ *COLOR CODE For Humans Agents:* Yellow = Susceptible | Red = Infected | Green = Exposed | Blue = Removed (Recovered/Isolated)
+ Parameters can be changed within the model itself using several different variable sliders.


### How do I run it?
+ Firstly install mesa here (along with python): https://mesa.readthedocs.io/en/latest/
+ Once installed, simply invoke `python3 disease_run.py` in the directory of the folder and the model will launch in browser.

### Credits
+ Dr Chalk for the introduction into AGM Simulation and MESA: https://www.youtube.com/watch?v=VeQkhfDYyMc&ab_channel=HSMA
+ Dr Akwafuo for advising the research done; https://www.sampsonakwafuo.com/home
+ The team behind the python framework aka Project MESA: https://mesa.readthedocs.io/en/latest/
+ William Blair for initial setting up of the model: https://www.linkedin.com/in/william-blair-2318451b3/