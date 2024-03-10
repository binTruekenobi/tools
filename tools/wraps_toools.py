import numpy as np
import matplotlib.pyplot as plt
import time

"""
decorator library for function runtimes
"""


def plot_vals(N=100, print_average=False):
    """
    plots the returned value for N iterations
    works only for functions which return numeric values
    can print the average value returned
    e.g. if you have a counter for a sorting alg, this can return the
    average number of that counter upon finish
    """
    def plott(func):
        def wrapper(*args, **kwargs):
            plots = np.empty((N, 2))
            su = 0
            for i in range(0, N):
                plots[i] = np.array([i, func(*args, **kwargs)])
                su += plots[i][1]

            if print_average:
                print(su/N)

            x = plots.transpose()
            plt.plot(x[0], x[1])
            plt.show()
        return wrapper
    return plott


"""
times a function.
should be fairly close to the actual runtime.
can return the function value
"""


def run_time(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        ret = func(*args, **kwargs)
        fin = time.time()
        exec_time = fin-start
        return (exec_time, ret)
    return wrapper



"""
plots or returns a list of runtimes for various values of n
the plot can give a good indication of O(n) for the function
"""


def O_n(check_vals=[2, 10, 100, 1000, 10**6],
        var_pos=0, plot=True, ret_vals=False):
    def outer(func):
        def wrapper(*args, **kwargs):
            print(args)
            ret_list = []
            for i in check_vals:
                args = ([j for j in args].insert(var_pos, i))
                print(args)
                ret_list.append(func(*args, **kwargs))
            if plot:
                plt.plot(check_vals, ret_list)
                plt.show()
            if ret_vals:
                return ret_list
        return wrapper
    return outer


"""
converts an argument to another type, if possible
"""
"""
*args are tuples and **kwargs are dicts so there are different converters 
"""

def conv_args(index, newtype):
    def outer(func):
        def wrapper(*args, **kwargs):
            f = args[index]
            try:
                x = newtype(f)
            except ValueError:
                raise ValueError("cannot cast", f, "of type",
                                type(f), "to", newtype)
            finally:
                args_list = [i for i in args]
                args_list[index] = x
                ret = func(tuple(args_list), **kwargs)
            return ret
        return wrapper
    return outer

def conv_kwargs(var_name, newtype):
    def outer(func):
        def wrapper(*args, **kwargs):
            f = kwargs[var_name]
            try:
                x = newtype(f)
            except ValueError:
                raise TypeError("cannot cast", f, "of type", 
                                type(f), "to", newtype)
            finally:
                kwargs[var_name] = x
                ret = func(args, kwargs)
            return ret
        return wrapper
    return outer