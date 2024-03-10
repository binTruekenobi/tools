"""
polynommial class with root finding algorithm
used for eigenvalues in the vectors_tool
"""
import imaginary_tools as imt
from math import sqrt
class polynomial():
    def __init__(self, coeffs):
        self.coeffs = coeffs
        self.order = len(self.coeffs)
        self.even = bool((self.order)%2)
        self.remove_zeros()
    def remove_zeros(self):
        reached_first = False
        trailing_zeros = 0
        for i in self.coeffs:
            if i != 0:
                reached_first = True
                break
            if i == 0 and reached_first == False:
                trailing_zeros += 1
        for j in range(0, trailing_zeros):
            del self.coeffs[0]
        self.order = len(self.coeffs)
    def poly(self, x):
        y = 0
        for i in range(1, len(self.coeffs)+1):
            #coeffs = [1, 2, 3, 4], x^3 + 2x^2 + 3x + 4
            y += self.coeffs[-i] * x**(i-1)
        return y
    def solve(self, real=True, hint = None):
        """
        find roots of the polynomial
        can return:
            lists of numerical roots,
            None,
            "all"
            lists of the complex class from imaginary_tools
        """
        if self.order == 0:
            self.roots = None
            return self.roots
        if self.order == 1:
            if self.coeffs == 0:
                self.roots = "all"
                return self.roots
            else:
                self.roots = None
                return self.roots
        if self.order == 2:
            self.roots = [-self.coeffs[1]/self.coeffs[0]]
        if self.order == 3:
            a = self.coeffs[0]
            b = self.coeffs[1]
            c = self.coeffs[2]
            desc = b**2 - 4*a*c
            if desc > 0:
                self.roots = [(-b+sqrt(desc))/(4*a), (-b-sqrt(desc))/(4*a)]
                return self.roots
            elif desc == 0:
                self.roots = [-b/(4*a)]
            else:
                if real == True:
                    self.roots = None
                    return self.roots
                else:
                    r = -b/(4*a)
                    c = sqrt(-desc)/(4*a)
                    self.roots = [imt.imaginary(r, c), imt.imaginary(r, -c)]
    def newton_raphson(self, start=0, num=50, retry = False, close = 10**-8, 
                       quit_when_close = True, close_d = 10**-8, hint = None):
        """
        add a check for if next iteration gives the same value
        /if f(n)/f'(n) = 0 
        """
        d = self.derivative()
        x_n = start
        root = None
        for i in range(0, num):
            if -close<self.poly(x_n)<close:
                root = x_n
                break
            if close_d<d.poly(x_n)<close_d:
                if -close<self.poly(x_n)<close:
                    root = x_n
                    break
                else:
                    print("hit stationary point")
                    if retry == False:
                        break
                    else:
                        #will break if it always hits s_p when start = 1, and retry == True
                        root = self.newton_raphson(start=1, num=num, retry=retry, close=close, 
                                    quit_when_close = True, close_d = close_d, hint=None)
            x_n = x_n - self.poly(x_n)/d.poly(x_n)
        return root
    def newton_raphson_simplify(self, n_r_soln):
        """
        simplifies the polynomial by x-root when newton_raphson called
        until a quartic is hit, which is then analytically solved
        for the other <5 roots
        """
        pass
    def newton_raphson_all_roots(self):
        self.even
        pass
    def derivative(self):
        coef_deriv = []
        for i in range(2, len(self.coeffs)+1):
            #coeffs = [1, 2, 3, 4], deriv = 3x^2 + 4x + 3
            coef_deriv.append(self.coeffs[-i]*(i-1))
        coef_deriv = [coef_deriv[-i] for i in range(1, len(self.coeffs))]
        self.deriv = polynomial(coef_deriv)
        return self.deriv
    def mult(self, p, rounding = False):
        """
        rounding can be set to an integer which rounds every number
        returned, can help to avoid floating point operating errors
        """
        highest_pow = self.order-1 + p.order-1
        """
        takes two polynomials and returns their product
        iterate over this for calculating eigenvalues in vector_tools
        """
        p1 = []
        p2 = []
        for i in range(0, self.order):
            p1.insert(0, [self.coeffs[-i-1], i])
        for j in range(0, p.order):
            p2.insert(0, [p.coeffs[-j-1], j])
        p3 = []
        for i in p1:
            for j in p2:
                p3.append([i[0]*j[0], i[1]+j[1]])
        product = [[0, highest_pow-k] for k in range(0, highest_pow)]
        product.append([0, 0])
        for i in p3:
            product[highest_pow-i[1]][0]+=i[0]
        if rounding == False:
            product_1d = [k[0] for k in product]
        else:
            if type(rounding) == int:
                product_1d = [round(k[0], rounding) for k in product]
            else:
                raise TypeError("Error: rounding takes int values only")
        poly_product = polynomial(product_1d)
        return poly_product
    def show(self, var):
        var = str(var)
        retstr = ""
        for i in range(0, self.order):
            const = self.coeffs[i]
            power = self.order-i+1
            
            if power == 1:
                partial_str
            
            
            if self.coeffs[i] == 1:
                partial_str = str(var) + "**" + str(self.order-i-1) + "+"
            elif self.order-i-1 == 1:
                partial_str = str(self.coeffs[i])
                
            partial_str = str(self.coeffs[i]) + "*" + str(var) + "**" + str(self.order-i-1) + "+"
            retstr+=partial_str
        return retstr
        