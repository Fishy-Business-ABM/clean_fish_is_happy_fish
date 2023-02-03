from SALib.sample import sobol
from SALib.analyze import sobol as sb
from mesa.batchrunner import BatchRunner
from model import Model
from clustering_coeff import get_average_clustering
import pandas as pd
from math import trunc
from execute import output_data
from itertools import combinations
import numpy as np
import matplotlib.pyplot as plt

problem = {
    'num_vars': 5,
    'names': ["food","reproduction","nb_sharks","mass_fish","regrowth_rate"],
    'bounds': [[1, 50], [0.001, 0.1], [1, 10], [0.00001, 0.001], [0.001, 0.01]]
}

# Set the repetitions, the amount of steps, and the amount of distinct values per variable
replicates = 2
max_steps = 10
distinct_samples = 2

# We get all our samples here
param_values = sobol.sample(problem, distinct_samples, calc_second_order=False)

count = 0
data = pd.DataFrame(index=range(replicates*len(param_values)), columns=problem["names"])
data['Run'], data['Clustering'] = None, None

for i in range(replicates):
    for vals in param_values: 
        # Change parameters that should be integers
        vals = list(vals)
        vals[0] = int(vals[0])
        vals[2] = int(vals[2])
        # Transform to dict with parameter names and their values
        variable_parameters = {}
        for name, val in zip(problem['names'], vals):
            variable_parameters[name] = val

        iteration_data = output_data(*vals, max_steps)
        data.iloc[count, 0:len(vals)] = vals
        data.iloc[count, len(vals):len(vals)+1] = count
        data.iloc[count, len(vals)+1:len(vals)+len(iteration_data)+1] = iteration_data
        count += 1

        print(f'{count / (len(param_values) * (replicates)) * 100:.2f}% done')

Si_clustering = sb.analyze(problem, data['Clustering'].values,
                            print_to_console=True, calc_second_order=False)

def plot_index(s, params, i, title=''):
    """
    Creates a plot for Sobol sensitivity analysis that shows the contributions
    of each parameter to the global sensitivity.

    Args:
        s (dict): dictionary {'S#': dict, 'S#_conf': dict} of dicts that hold
            the values for a set of parameters
        params (list): the parameters taken from s
        i (str): string that indicates what order the sensitivity is.
        title (str): title for the plot
    """

    indices = s['S' + i]
    errors = s['S' + i + '_conf']
    plt.figure()

    l = len(indices)

    plt.title(title)
    plt.ylim([-0.2, len(indices) - 1 + 0.2])
    plt.yticks(range(l), params)
    plt.errorbar(indices, range(l), xerr=errors, linestyle='None', marker='o')
    plt.axvline(0, c='k')


plot_index(Si_clustering, problem['names'], '1', 'First order sensitivity')
plt.show()

plot_index(Si_clustering, problem['names'], 'T', 'Total order sensitivity')
plt.show()
    