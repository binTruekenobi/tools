import sys
sys.path.insert(0, r"insert taylor series file path here")

import taylor_series_function as ts


import polynomial_tools as pt

def function(x):
    return x**2

def integrate_ts(L, U, function, steps, terms=4):
    """
    integral using nth order taylor approximations
    
    e.g. integrate_ts(1, 3, function, 1000)
    """
    integral = 0
    for i in range(0, steps):
        val = L + i*(U-L)/steps
        #print(val)
        tay = ts.taylor(function, val, terms, show_taylor = True, rnd = 4, simplify=True)
        #print("T:", tay)
        obj_t = pt.polynomial(tay)
        obj_int = obj_t.integral()
        #print(obj_int)
        integral += obj_int.poly(val+(1/steps))-obj_int.poly(val)
        #print("int: ", integral)
    return integral*(U-L)
