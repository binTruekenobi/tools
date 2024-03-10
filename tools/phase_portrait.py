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


@vt.gen2d(-5, 5, 30, 0, 1)
def t(a, b):
    return a

def low_dim(l):
    return [i[0] for i in l]

def remove_mults(l):
    seen = [l[0]]
    for i in l:
        can_add = True
        for j in seen:
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
        pass
    scale = 1/min(x)
    if min(x) != min(l):
        scale = -scale
    return [scale*i for i in l]
        
def phase_plot(A, eig_plt = False):
    mat_A = vt.square_matrix()
    x = []
    y = []
    x_dir = []
    y_dir = []
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
            if len(f.eigenvecs)>0:
                if len(evs) == 0:
                    evs.append(f.eigenvecs)
                else:
                    p = f.eigenvecs
                    for i in evs:
                        if p[0][0] == 0  or p[0][1] == 0:
                            continue
                        else:
                            if i[0][0]/p[0][0] != i[0][1]/p[0][1]:
                                evs.append(f.eigenvecs)
                                break
        
    evs = low_dim(evs)
    evs = remove_mults(evs)
    if len(evs) == 1:
        evs = evs[0]
        evs = set_first_1(evs)
    evs = [simplify(l) for l in evs]
    if eig_plt:
        plt.quiver([0 for i in evs], [0 for i in evs], [i[0] for i in evs], [i[1] for i in evs], scale=1, width=0.002)
        plt.quiver([0 for i in evs], [0 for i in evs], [-i[0] for i in evs], [-i[1] for i in evs], scale=1, width=0.002)
    print(evs)
    plt.quiver(x, y, x_dir, y_dir)
phase_plot([[1, -2], [1, -2]], True)


