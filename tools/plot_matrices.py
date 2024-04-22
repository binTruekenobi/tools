import vectors_tool as vt
import plot_functions as pf

"""
plots v^T M v for v taking values with the x and y ranges
"""

matrix = [[1, 1], [1, 1]]
vec = vt.matrix_vecmult(matrix)
def function(x, y):
    return vec.multv([x, y])

def plot_matrix(Lx, Ux, Sx, Ly=None, Uy=None, Sy=None):
    pf.plot_function_3d(function, Lx, Ux, Sx, Ly=Ly, Uy=Uy, stepsy=Sy)

plot_matrix(-5, 5, 100)
