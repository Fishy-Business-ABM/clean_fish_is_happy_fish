# Partly written by ChatGPT

import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from math import pi, exp

# Define the linear function
def levi(x_data, c):
    y_data = []
    for x in x_data:
        if x == 0:
            y_data.append(0)
        else:
            y_data.append(((c / (2 * pi)) ** 1/2) * exp(-c / (2 * x)) / (x ** 3/2))
    return np.array(y_data)

def fit(x_data, y_data, function):
    # Fit the function to the data
    param, cov = curve_fit(function, x_data, y_data)

    # Predict the values using the fitted function
    y_pred = function(x_data, *param)

    # Calculate the R-squared value
    r_squared = 1 - ((y_data - y_pred) ** 2).sum() / ((y_data - y_data.mean()) ** 2).sum()

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

    return (float(param[0]),float(r_squared))