# Fishy business - An agent-based model of flocking behaviour in fish

TODO: introduction

## Getting started

### Prerequisites

TODO: modules and stuff

### Repository

The following files contain the most important parts of the program.
- **model.py**: describes the environment of the ABM. It contains code to add and remove agents (i.e., fish and sharks), to update environment elements (e.g., regrowing food) and to step the model.
- **food.py**: contains code that defines how the fish's food sources regrow.
- **fish.py**: describes the behaviour of the fish. It contains movement rules (i.e., Boids rules, attraction to food and repulsion from sharks), a sexual reproduction mechanism and metabolism.
- **shark.py**: describes the behaviour of the sharks. It contains movement rules (i.e., a direction-constrained random walk if no fish is in sight, and attraction to the closest fish otherwise) and removes fish that are being eaten.
- **execute.py**: contains a function that runs the model for a given number of iterations, with a number of model parameters as input and parameterized output variables of the model.
- **visualization.py**: contains a visualization of the model that runs and visualizes in real-time.
- **OFAT.py**: contains code to run a One Factor at a Time analysis of the model. It writes the output to a .txt file.
- **sobol.py**: contains code to run a Global Sensitivity Analysis. It writes the output to a .txt file.
- **plots**: contains a number of plots regarding the learned behaviour of the fish.
- **results**: contains the sensitivity analysis data used to generate the plots.

## Visualization

TODO

## Sensitivity analysis

### One Factor at a Time

The One Factor at a Time (OFAT) analysis takes into account the following five intput parameters:
- Number of food sources
- Reproduction rate of the fish
- Number of sharks
- Mass of the fish (the higher the mass, the faster the fish can swim and the more energy it loses per step)
- Regrowth rate of the food
And it outputs the following variables:
- An estimate of the flocking index over the last 100 steps of the model.
- The genes of all fish, representing the learned behaviour of the fish.
- The number of fish present at the end of the model execution.

To run the OFAT analysis, execute the following command.
```
python OFAT.py
```
Your machine will now fix the last four parameters, and vary the first parameter. For each value of the first parameter, it runs the model 10 times for 1000 steps and write the output variables to a .txt file in the Results directory. Consequently, it fixes parameters 1 and 3-5 and varies parameter 2, etcetera until all parameters have been analysed. During the analysis, the program prints the progress in your terminal by stating which parameter it is varying and what value it is currently giving to the parameter.

TODO: how to make plots

### Global Sensitivity Analysis

An OFAT analysis only takes into account the variation in output if one input parameter is independently changed. A Global Sensitivity Analysis (GSA) studies how different parameters interact to determine the output of the model. The GSA takes into account the same input parameters and output variables as the OFAT analysis.

To run the GSA, execute the following command.
```
python sobol.py
```
Your machine will now create a Sobol sequence (i.e., a quasi-random set of point in the input parameter space) and execute the model 10 times for 1000 steps for each parameter setting in the Sobol sequence. It repeats this process 10 times and stores the output variables. Afterwards, the SALib module is called to analyse the data and two plots are generated for each output variable: the first order index and the total order index. During the analysis, the program prints its progress in your terminal.
