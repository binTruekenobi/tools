import vectors_tool as vt
import matplotlib.pyplot as plt




"""
import polynomial_tools as pt

for eigenvals, create poly lambda - eigenval and mult() until largest possible eqn formed

char_eqn = poly([1])
for i in evals:
    x = poly(1, -i)
    char_eqn = char_eqn.mult(x)
return char_eqn.show(lambda λ)
return eqn

"""

e=0

A = [[1, 3], [-1, 1+e]]

def trace_path(A, start, N=20, move = None):
    if move == None:
        move = 1/N
    x, y = start[0], start[1]
    positions = [[x, y]]
    for i in range(0, 15*N):
        f = vt.mat_vec(A, [x, y])
        deriv = f.multiply()
        disp = [move*j for j in deriv]
        x+= disp[0]
        y+= disp[1]
        if not (abs(x)>lm+1 or abs(y) > lm+2):
            positions.append([x, y])
    plot_vals_x = [i[0] for i in positions]
    plot_vals_y = [i[1] for i in positions]
    plt.plot(plot_vals_x, plot_vals_y, color="b")
        
#trace_path([[1, -1], [1, -2]], [-1, 4])

lm = 10



@vt.gen2d(-lm, lm, 2*lm, 0, 1)
def t(a, b):
    return a


@vt.gen2d(-lm, lm, lm, 0, 1)
def n(a, b):
    return a

x = n(1, 2)
for i in x:
    for j in i:
        trace_path(A, j)

def low_dim(l):
    return [i[0] for i in l]

def remove_mults(l):
    if len(l) == 0:
        return 0
    seen = [l[0]]
    for i in l:
        can_add = True
        for j in seen:
            if (i[1] == 0) ^ (i[0] == 0):
                continue
            elif i[1] == 0 and i[0] == 0:
                if [0, 0] not in seen:
                    seen.append([0, 0])
            else:
                if j[1]/i[1] == j[0]/i[0]:
                    can_add = False
        if can_add:
            seen.append(i)
    return seen

def set_first_1(l):
    if l[0] == 0:
        pass
    else:
        ratio = 1/l[0]
    return [i*ratio for i in l]

def simplify(l):
    x = [abs(i) for i in l]
    if min(x) == 0:
        return None
    scale = 1/min(x)
    if min(x) != min(l):
        scale = -scale
    return [scale*i for i in l]

def simplify_eigenvecs(eigenvecs):
    print(eigenvecs)
    if [0, 0] in eigenvecs:
        while [0, 0] in eigenvecs:
            eigenvecs.remove([0, 0])
    if len(eigenvecs) == 2:
        if eigenvecs[0][0] == 0:
            eigenvecs[0][1] = 1
        if eigenvecs[0][1] == 0:
            eigenvecs[0][0] = 1
        if eigenvecs[1][0] == 0:
            eigenvecs[1][1] = 1
        if eigenvecs[1][1] == 0:
            eigenvecs[1][0] = 1
    elif len(eigenvecs) == 1:
        if eigenvecs[0][0] == 0:
            eigenvecs[0][1] = 1
        if eigenvecs[0][1] == 0:
            eigenvecs[0][0] = 1

    for i in range(0, 2):
        if 0 not in eigenvecs[i]:
            abs_list = [abs(j) for j in eigenvecs[i]]
            thing_to_scale = min(abs_list)
            scale = 1/thing_to_scale
            new_list = [j*scale for j in eigenvecs[i]]
            eigenvecs[i] = new_list
            
    
    return eigenvecs
    
        
def phase_plot(A, eigs = False, eig_plt = False):
    if not eigs and eig_plt:
        raise ValueError("cannot do eig_plt with eigs set false")
    x = []
    y = []
    x_dir = []
    y_dir = []
    if eigs:
        evs = []
    iter8 = t(None, None)
    for i in iter8:
        for j in i:
            x.append(j[0])
            y.append(j[1])
            f = vt.mat_vec(A, list(j))
            prdct = f.multiply()
            x_dir.append(prdct[0])
            y_dir.append(prdct[1])
            #trace_path(A, j)
    if eigs:
        A_mat = vt.square_matrix(A)
        eigenvals = A_mat.two_d_case_eigenval()
        if eigenvals[0] == eigenvals[1]:
            print(eigenvals[0])
        else:
            print(eigenvals)
        eigenvecs = A_mat.two_d_case_eigenvec()
        eigenvecs = [eigenvecs[0].coord, eigenvecs[1].coord]
        if not type(eigenvecs[0]) == it.imaginary:
            eigenvecs = simplify_eigenvecs(eigenvecs)
        else:
            print("eigenvectors imaginary")
            print([(j.x, j.y) for j in i.coord] for i in eigenvecs)
        if len(eigenvecs) == 2:
            print(eigenvecs[0], eigenvecs[1])
        elif len(eigenvecs) == 1:
            print(eigenvecs[0])
        evs = eigenvecs
    if eig_plt:
        print(evs)
        plt.quiver([0 for i in evs], [0 for i in evs], [i[0]*lm for i in evs], [i[1]*lm for i in evs], scale=1, width=0.003, color = "r")
        plt.quiver([0 for i in evs], [0 for i in evs], [-i[0]*lm for i in evs], [-i[1]*lm for i in evs], scale=1, width=0.003, color = "r")
    #print(evs)
    plt.quiver(x, y, x_dir, y_dir)
    
phase_plot(A, False, False)

