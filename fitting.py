# Partly written by ChatGPT

import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from math import pi, exp
from execute import execute

# Define the linear function


def levi(x_data, c):
    y_data = []
    for x in x_data:
        if x == 0:
            y_data.append(0)
        else:
            y_data.append(((c / (2 * pi)) ** 1/2) *
                          exp(-c / (2 * x)) / (x ** 3/2))
    return np.array(y_data)


def fit(x_data, y_data, function):
    # Fit the function to the data
    param, cov = curve_fit(function, x_data, y_data)

    # Predict the values using the fitted function
    y_pred = function(x_data, *param)

    # Calculate the R-squared value
    r_squared = 1 - ((y_data - y_pred) ** 2).sum() / \
        ((y_data - y_data.mean()) ** 2).sum()

    # Plot the data and the fitted function
    plt.scatter(x_data, y_data, label='Data')
    plt.plot(x_data, function(x_data, *param), 'r-', label='Fitted Function')

    # Add labels and title
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Linear Function Fit')
    plt.legend()

    # Show the plot
    plt.show()

    return (float(param[0]), float(r_squared))


def fit_levi_to_shark(id, out_shark, precision):
    step_lengths = []
    for time in range(len(out_shark)):
        for shark in out_shark[time]:
            if shark["id"] == id:
                step_lengths.append(shark["step-size"])

    maximum = max(step_lengths)

    boxes = [i / precision * maximum for i in range(precision+1)]
    frequencies = [0 for _ in range(precision+1)]
    for step_length in step_lengths:
        frequencies[int((step_length / maximum) * precision)] += 1

    return fit(np.array(boxes), np.array(frequencies), levi)


out = execute(
    nb_food=10,
    nb_initial_fish=10,
    nb_sharks=1,
    mass_fish=0.0001,
    food_regrowth_rate=0.005,
    max_runtime=1000
)

param, r_squared = fit_levi_to_shark(out[2][0][0]["id"], out[2], 50)
print("Parameter: %f" % (param))
print("R-squared value: ", r_squared)
