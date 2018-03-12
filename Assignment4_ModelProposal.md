# Model Proposal for Blight Spread

Michael Borsellino

* Course ID: CMPLXSYS 530,
* Course Title: Computer Modeling of Complex Systems
* Term: Winter, 2018

&nbsp; 

### Goal 
*****
 
The goal is to model how blight spreads across space in dense urban areas.  I am interested in elucidating the intersection of blight with the built environment as physical decay and with the housing market as decay of value from potential capitalization..  

&nbsp;  
### Justification
****
The ABM is useful because for demonstrating how blight infilitrates and spreads through the environment.  Using relatively simply rules, the ABM is capable of demonstrating complex interactions between agents and their environment.

&nbsp; 
### Main Micro-level Processes and Macro-level Dynamics of Interest
****

I am interested in seeing how blight spreads and persists over time.  Clustering of blight in certain quadrants will especially important.  I will be assessing how blight spread and blight recovery stabilize each other.

&nbsp; 


## Model Outline
****
&nbsp; 
### 1) Environment

Boundary conditions are fixed to represent the city boundaries.  
This model has two dimensions.  A third could be added at a later date to better represent the complexity of urban housing variations.

This is a cellular automata where each cell represents a block of city housing.  Cells can have a state of 0, 1, or 2, representing recovering from blight, unblighted, and blighted and spreading.  (This is largely based off of pycx's host-pathogen model).  

&nbsp; 

### 2) Agents
 
 There are no agents as this is a cellular automata.

&nbsp; 

### 3) Action and Interaction 
 
**_Interaction Topology_**

Neighborhoods consist of the surround 8 adjacent cells.  That is, blight can spread to an adjacent cell in any direction.
 
**_Action Sequence_**

A cell on the grid searches it's neighbors.  If it is recovering from blight and adjacent to an unblighted cell, it's chance of becoming unblighted is determined by regrowthRate.  If it is adjacent to a blighted cell, it's chance of chance of becoming blighted (again) is determined by blightRate.  If it is not adjacent to a blighted or an unblighted cell, it remains in the recovering state.  The time order issue here needs improvement.


If the cell is unblighted and adjacent to a blighted cell, it's chance of becoming blighted is determined by blightRate.  If it is not adjacent to a blighted cell is remains unblighted.

If the cell is blighted, it transitions to recovering. This needs work, cells should not immediately transition to recovering.

__*LS COMMENTS:*__
*One way of handling this would be to make "blightness" a continuous variable that increments each turn according to some combination of a set rate and the influence of neighbors. Another way would be to make this a probabilistic recovery wherein a cell transitions from one state to another with a probability that is dependent on surrounding cells.*

*One think I was not sure of from this description is what happens to a cell if it is adjacent to both blighted and unblishted cells?  Also, does being adjacent to 3 blighted cells make a cell more likely to become blighted?*

The parameters (blightRate and regrowthRate) as well as the step procedure function are in section 4.

&nbsp; 
### 4) Model Parameters and Initialization

_Describe and list any global parameters you will be applying in your model._

The probability of starting as a blighted cell is defined by initProb. There are currently two interacting rates.  First, blightRate, which is how quickly blight spreads to surrounding neighborhoods.  Second, regrowthRate is how quickly blighted neighborhoods recover.  Both of these are adjustable parameters.  Initial conditions are listed below.  
```python
width = 50
height = 50
initProb = 0.0007
blightRate = 0.15
recoveryRate = 0.2
```
_Describe how your model will be initialized_

```python
def bRate (val = blightRate): #rate of blight spread to nearby city blocks, parameter can be changed in model

    global blightRate
    blightRate = float(val)
    return val

def rRate (val = recoveryRate): #rate of regrowth of blighted city blocks, parameter can be changed in model
 
    global recoveryRate
    recoveryRate = float(val)
    return val
    
def init():
    global time, config, nextConfig

    time = 0
    
    config = SP.zeros([height, width])
    for x in xrange(width):
        for y in xrange(height):
            if RD.random() < initProb:
                state = 2
            else:
                state = 1
            config[y, x] = state

    nextConfig = SP.zeros([height, width])

def draw():
    PL.cla()
    PL.pcolor(config, vmin = 0, vmax = 2, cmap = PL.cm.jet)
    PL.axis('image')
    PL.title('t = ' + str(time))
```

_Provide a high level, step-by-step description of your schedule during each "tick" of the model_

```python
def step():
    global time, config, nextConfig

    time += 1

    for x in xrange(width):
        for y in xrange(height):
            state = config[y, x]
            
            if state == 0:
                for dx in xrange(-1, 2):
                    for dy in xrange(-1, 2):
                        if 1 < y+dy%height < ((height * 2) - 2): #there has to be a better way to create fixed boundary
                        
## LS COMMENTS: I believe 0 <= y+dy <= (height - 1) and similarily for x should get you want you want; no need for modulo if you aren't # wrapping

                            if 1 < x+dx%width < ((width * 2) - 2):
                                if config[(y+dy)%height, (x+dx)%width] == 1:
                                    if RD.random() < recoveryRate:
                                        state = 1
                                 elif config[(y+dy)%height, (x+dx)%width] == 2: #time order issue, should recovering be more susceptible?

## LS COMMENTS: The time order issue might be an argument for treating "blightedness" as a continuous variable; it would allow each these processes to act simultaneously on one cell. This may not be what you are looking for, however.

                                    if RD.random() < blightRate:
                                        state = 2
                                       
            elif state == 1:
                for dx in xrange(-1, 2):
                    for dy in xrange(-1, 2):
                        if 1 < y+dy%height < ((height * 2) - 2):
                            if 1 < x+dx%width < ((width * 2) - 2):
                                if config[(y+dy)%height, (x+dx)%width] == 2:
                                    if RD.random() < blightRate:
                                        state = 2
                                
            else:
                state = 0 #blighted shouldn't transition immediately to recovering

            nextConfig[y, x] = state

    config, nextConfig = nextConfig, config

```
__*LS COMMENTS:*__

*As currently written, I am pretty sure that your new cell state is only be determined by the last neighboring cell that is checked in each loop (so here, it would be the cell at (x + 1, y +1)). I would suggest changing this to either a) a "totalistic" rule wherein you count up the neighbors in each state to decide what happenes next (see Game of Life for an example of this sort of rule) or b) make it so that you randomly pick one neighbor to be influenced by. Also, double check whethere you have synchronous or asychronous updating going on here. I can't quite tell currently, but you should make sure that whichever is going on is the one that you intend to be happening.*

&nbsp; 

### 5) Assessment and Outcome Measures

I am most interested in seeing how blight diffuses and clusters in the environment. I need to figure out a better way to measure this objectively.  

__*LS COMMENTS:*__
*I'd suggest looking at the way the notebook the Schelling model uses to get at a measure of segregation. Also, just a raw percentage of blighted in a system will also be informative*
&nbsp; 

### 6) Parameter Sweep

I think this is referring to what parameters will be adjusted when testing the model.  This would be blightRate and regrowthRate - the rates of spread of and recovery from blight.  Based on early runs, their realistic range is relatively small, potentially between 0.0 and 0.2 for each.  I'll push that a little bit wider to ensure comprehensiveness.  Any more blight and the city becomes an untamed disaster zone, and faster recovery just isn't feasible.

__*LS COMMENTS:*__
*Another parameter to consider is how the model is initialized. Currently, random spots begin as blighted with a certain level of probility. What percentage begins blighted and whether or not blight starts out in clusters will be important to consider here.
