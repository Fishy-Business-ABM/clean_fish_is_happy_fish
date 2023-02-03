from execute import output_clustering
from copy import copy
from statistics import mean, variance
import numpy as np
import pandas as pd


params_to_change = ["food","reproduction","nb_sharks","mass_fish","regrowth_rate"]

def OFAT(default_values, test_values, nb_iterations, steps_per_iteration):
    assert len(default_values) == len(test_values)

    stats = []

    for i_param in range(len(default_values)):
        print("Parameter %i" %(i_param))
        values = copy(default_values)
        stats_per_param = []
        for i_value in range(len(test_values[i_param])):
            print("Value %i" %(i_value))
            values[i_param] = test_values[i_param][i_value]

            outs = [test_values[i_param][i_value]]
            for _ in range(nb_iterations):
                outs.append(output_clustering(*values, steps_per_iteration))
                #print(outs[-1])
            #avg = mean(outs)
            #print(avg)
            #var = variance(outs)
            stats_per_param.append(outs)
        with open(params_to_change[i_param] +"_full2.txt", "w") as file:
            file.write(params_to_change[i_param]+ "\n")
            file.write(str(stats_per_param))
        stats.append(stats_per_param)

    
    return stats

print(OFAT([30,                             # default nb_food
            0.01,                           # default reproduction rate
            3,                              # default nb_sharks
            0.0001,                         # default mass_fish
            0.005],                         # default regrowth_rate
            [range(10,50,5),                # test values nb_food
            np.arange(0.005,0.05,0.005),    # test values reproduction
            range(1,5,1),                   # test values nb_sharks
            np.arange(0.00001,0.001,0.0001),# test values mass_fish
            np.arange(0.001,0.01,0.001)],   # test values regrowth_rate
            30,                             # nb_iterations
            1000))                          # steps_per_iteration

