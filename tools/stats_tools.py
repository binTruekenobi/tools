from math import pi, sqrt
import numpy as np
def run_as_population(func):
    def wrapper(*args, **kwargs):
        args = ([i for i in args].append(True))
        result = func(*args, **kwargs)
        return result
    return wrapper

def run_as_sample(func):
    def wrapper(*args, **kwargs):
        args = ([i for i in args].append(False))
        result = func(*args, **kwargs)
        return result
    return wrapper

def simulate_normal(sigma, mu, lower=None, upper=None, chops=1000):
    if lower == None and upper == None:
        raise AssertionError("cannot have both lower and upper sums 0")
    elif lower != None and upper == None:
        x_values = np.linspace(lower, 10, num=chops)
        x_scale = 10 - lower
    elif lower == None and upper != None:
        x_values = np.linspace(-10, upper, num=chops)
        x_scale = upper+10
    else:
        x_values = np.linspace(lower, upper, num=chops)
        x_scale = upper-lower
    x_scale *= 1/chops
    normalise = 1/(sigma*sqrt(2*pi))
    y_vals = (-1/2) * ((x_values - mu)/sigma)**2
    height = np.exp(y_vals)
    integral = np.sum(height)
    integral*=normalise
    integral*= x_scale
    return integral

def factorial(x):
    val = 1
    for i in range(2, x+1):
        val*=i
    return val
def gamma_function(x, stopval = 1000, chops = 10000):
    if x == float(int(x)):
        return factorial(int(x-1))
    x_vals = np.linspace(0, stopval, num=chops)
    y_vals = x_vals**(x-1)
    x_negative = -x_vals
    f_vals = y_vals * np.exp(x_negative)
    func = f_vals * stopval/chops
    area = np.sum(func)
    return area
    
def student_t(t, v):
    gam1 = gamma_function((v+1)/2)
    gam2 = gamma_function(v/2)
    p1 = gam1/(sqrt(v*pi)*gam2)
    p2 = (1 + (t**2)/v)**(-(v+1)/2)
    f_val = p1*p2
    return f_val

def student_t_pdf(t, v, chops=10000):
    x = np.linspace(0, t, num = chops)
    
    y = np.array([student_t(i, v) for i in x])
    return 2*np.sum(y)/chops


class stat():
    def __init__(self, data, population=True):
        self.data = data
        self.size = len(data)
        self.mean = sum(data)/self.size
        self.ordered_data = sorted(data)
        if population:
            self.population()
        else:
            self.sample
        if self.size == 1:
            self.median = self.mode = self.mean
    def __str__(self):
        return f'({self.data})'
    def population(self):
        self.population = True
    def sample(self):
        self.population = False
    def change_datatype(self):
        if self.sample:
            del self.sample
            self.population()
        elif self.population:
            del self.population
            self.sample()
        else:
            raise AttributeError("data of neither sample of population type cannot switch type, set type first")
    def variance(self):
        var = sum([(i-self.mean)**2 for i in self.data])
        #self.var = var/(self.size-int(hasattr(self, self.population)))
        if self.sample:
            normalise = 1/(self.size - 1)
        else:
            normalise = 1/(self.size)
        self.var = var/normalise
        return self.var
    def median(self):
        if self.size%2:
            self.median = self.ordered_data[(self.size+1)/2]
        else:
            two_points = [self.ordered_data[self.size/2], [self.ordered_data[(self.size/2)+1]]]
            self.median = sum(two_points)/2
        return self.median
    def mode(self, cuttoff_val = False):
        values_list = []
        values_freq = []
        modes = []
        for i in self.data:
            if i not in values_list:
                values_list.append(i)
                values_freq.append(0)
            else:
                values_freq[values_list.index(i)]+=1
        highest_freq = max(values_freq)
        if highest_freq == 1:
            return []
        for i in range(0, len(values_freq)):
            if values_freq[i] == highest_freq:
                modes.append(values_list[i])
        if not cuttoff_val and len(modes)>cuttoff_val:
            return None
        else:
            return modes
    def LQ(self):
        pos = (self.size+1)/4
        if pos == float(int(pos)):
            self.LQ = self.data[pos]
        elif pos-int(pos) == 0.25:
            x = int(pos)-1
            self.LQ = (3*self.data[x] + self.data[x+1])/4
        elif pos-int(pos) == 0.5:
            x = int(pos)-1
            self.LQ = (self.data[x] + self.data[x+1])/2
        elif pos - int(pos) == 0.75:
            x = int(pos)-1
            self.LQ = (self.data[x] + 3*self.data[x+1])/4
        return self.LQ

class two_sets():
    def __init__(self, X, Y):
        self.X = np.array(X)
        self.Y = np.array(Y)
        self.X_data = stat(X)
        self.Y_data = stat(Y)
    def covariance(self):
        XY = self.X * self.Y
        E_XY = np.sum(XY)/len(self.X)
        self.covariance = E_XY - self.X_data.mean*self.Y_data.mean
        return self.covariance