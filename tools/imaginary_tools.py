import math


"""argand equivalent of imaginary,
argument and moduli are in the initiator function of imaginary
argand_form stores them and allows conversion backway only
"""
class argand_form():
    def __init__(self, r, theta):
        self.r = r
        self.theta = theta
    def conv_imag(self):
        self.imag = imaginary(self.r*math.sin(self.theta), self.r*math.cos(self.theta))

"""
redifined imaginary class with more operations than the standard library
returns values either as subclasses (mostly just imaginary) or as lists.
"""
class imaginary():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.arg()
        self.moduli = math.sqrt((self.x)**2 + (self.y)**2)
    def mod(self):
        return self.moduli
    def arg(self):
        rough_tan = math.atan((self.y)/(self.x))
        pie = math.pi
        if self.x < 0 and self.y > 0:
            self.argument = pie + rough_tan
        elif self.x < 0 and self.y < 0:
            self.argument = rough_tan - pie
        else:
            self.argument = rough_tan
    def log(self):
        self.lnmod = math.log(self.moduli)
        self.logarithm = imaginary(self.lnmod, self.argument)
        return(self.logarithm.x, self.logarithm.y)
    def conv_arg(self):
        return (self.moduli, self.argument)
    def conj(self):
        self.conjugate = imaginary(self.x, -self.y)
        return (self.conjugate.x, self.conjugate.y)
    def conv_imag(self, size, rotate):
        x_coord = size*math.cos(rotate)
        y_coord = size*math.sin(rotate)
        return (x_coord, y_coord)
    def exp_hidden(self, x, y):
        exp_size = math.exp(x)
        exp_spinny = y
        ret_vals = self.conv_imag(exp_size, exp_spinny)
        return (ret_vals)
    def exp(self):
        return self.exp_hidden(self.x, self.y)
    """e^itheta = cos(theta) + i sin(theta)
    re^itheta + re^-(I IS IMPORTANT)itheta = 2rcos(theta)
    currently returns trig as a list,
    maybe make them subclasses?
    to add:
        all other trig funcs
        invert(finished) - sec, cot, e.t.c
        squares (done)
        powers
        uh
        matrices (use exp_mat import etc)

    todo:
        rearange like:
            __init__

            mod, arg, big properties and stuff

            math, add, square, (done)

            trig (finished first 3)

            log/exp

            misc
    to make:
        add plot functionality - separate import
        add general matrix functionality - rename numpy
        make general matrix functionality import  work for complex numbers
        import this into that and vice versa
    """
    """
    current bugs:

    1.
    some functions requiring self._something_ only defined in
    non-initiator functions requires these functions to be ran first

    solutions:

    force all functions to run at the start

    force all functions to run in the requiring function, iff function not ran
    e.g. initialise all to None if not specified, check if None at the start
    cons:
        slow?

    define them all at the start
    cons:
        no more functions

    do nothing about it
    cons:

    current solution:
        force functions to run in requiring function,
        shift the more important ones into the initiator

    """
    def sin(self):
        e1 = self.exp_hidden(-self.y, self.x)
        e2 = self.exp_hidden(self.y, -self.x)
        ret_sin = [(e1[0]-e2[0])/2, (e1[1] + e2[1])/2]
        return ret_sin
    def cos(self):
        e1 = self.exp_hidden(-self.y, self.x)
        e2 = self.exp_hidden(self.y, -self.x)
        ret_cos = [(e1[0]+e2[0])/2, (e1[1] +e2[1])/2]
        return ret_cos
    def tan(self):
        ret_sin = self.sin(self)
        sinclass = imaginary(ret_sin[0], ret_sin[1])
        ret_cos = self.cos(self)
        cosclass = imaginary(ret_cos[0], ret_cos[1])
        tanlist = sinclass.divide(cosclass.x, cosclass.y)
        return tanlist
    def inv(self):
        self.conj()
        self.inverse = imaginary(self.conjugate.x/(self.moduli**2), self.conjugate.y/(self.moduli**2))
        return [self.inverse.x, self.inverse.y]

    def sq(self):
        self.square = imaginary(self.x**2 -self.y**2, 2*self.x*self.y)
        return [self.square.x, self.square.y]
    def mult(self, x_2, y_2, *, makeclass = False):
        ret_list =  [(self.x*(x_2)-self.y*(y_2)), (self.x*(y_2)+self.y*(x_2))]
        if makeclass:
            self.multi = imaginary(ret_list[0], ret_list[1])
        return ret_list
    def divide(self, x_2, y_2):
        placehold = imaginary(x_2, y_2)
        listplace = placehold.inv()
        return self.mult(listplace[0], listplace[1])
    def add(self, x_2, y_2):
        return [self.x+x_2, self.y+y_2]
    def subtract(self, x_2, y_2):
        return [self.x-x_2, self.y-y_2]
