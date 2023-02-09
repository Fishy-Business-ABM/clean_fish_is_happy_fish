from execute import output_data
from copy import copy
from statistics import mean, variance
import numpy as np
import pandas as pd

params_to_change = ["food","reproduction","nb_sharks","mass_fish","regrowth_rate"]

def OFAT(default_values, test_values, nb_iterations, steps_per_iteration):
    assert len(default_values) == len(test_values)

    for i_param in range(len(default_values)):
        with open(params_to_change[i_param] +"_full3.txt", "w") as file:
            file.write("ParameterValue,flocking index,Gene0_avg,Gene0_std,Gene1_avg,Gene1_std,Gene2_avg,Gene2_std,Gene3_avg,Gene3_std,Gene4_avg,Gene4_std,number_fish\n")

            print("Parameter %i" %(i_param))
            values = copy(default_values)
            stats_per_param = []
            for i_value in range(len(test_values[i_param])):
                print("Value %i" %(i_value))
                values[i_param] = test_values[i_param][i_value]
                for i in range(nb_iterations):
                    line = str(values[i_param])
                    outs = output_data(*values, steps_per_iteration)
                    for out in outs:
                        line += ',' + str(out)
                    file.write(line + '\n')
            

OFAT([30,                             # default nb_food
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
     1000)                           # steps_per_iteration

