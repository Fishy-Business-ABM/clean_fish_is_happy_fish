from execute import output_clustering
from copy import copy
from statistics import mean, variance
import numpy as np

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

            outs = []
            for _ in range(nb_iterations):
                outs.append(output_clustering(*values, steps_per_iteration))
                print(outs[-1])
            avg = mean(outs)
            print(avg)
            var = variance(outs)
            stats_per_param.append((avg,var))
        stats.append(stats_per_param)
    
    return stats

print(OFAT([10,                             # default nb_food
            50,                             # default nb_initial_fish
            1,                              # default nb_sharks
            0.0001,                         # default mass_fish
            0.005],                         # default regrowth_rate
            [range(1,10,1),                 # test values nb_food
            range(10,100,10),               # test values nb_initial_fish
            range(1,3,1),                   # test values nb_sharks
            np.arange(0.0001,0.001,0.0001), # test values mass_fish
            np.arange(0.001,0.01,0.001)],   # test values regrowth_rate
            5,                              # nb_iterations
            10))                           # steps_per_iteration

