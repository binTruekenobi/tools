import numpy as np
import matplotlib.pyplot as plt

def function(x):
    """
    function example
    """
    return x**2

def function_3d(x, y):
    """
    example function for 3d plots
    """
    return x+y

def plot_function(function, L, U, steps):
    """
    plot a function between L and U with n steps
    """
    x = np.linspace(L, U, steps)
    #while y = function(x) often works, to ensure it for all functions, we iterate over x 
    #as not everything can be vectorised
    y = np.array([function(i) for i in x])
    plt.plot(x, y)


def plot_function_3d(function, Lx, Ux, stepsx, Ly=None, Uy=None, stepsy=None):
    """
    plot a function in 3d space between Lx and Ux, and Ly and Uy with stepsx and stepsy steps
    if Ly, Uy, stepsy are not specified, they will match what is input for x
    """
    if Ly == Uy == stepsy == None:
        Ly = Lx
        Uy = Ux
        stepsy = stepsx
    
    x_values =  np.linspace(Lx, Ux, stepsx)
    y_values = np.linspace(Ly, Uy, stepsy)
    x, y = np.meshgrid(x_values, y_values)
    #again, while function(x, y) can sometimes work, it's more reliable to iterate over the list
    f = np.array([[function(x, y) for x in x_values] for y in y_values])
    ax = plt.axes(projection='3d')
    ax.plot_surface(x, y, f)