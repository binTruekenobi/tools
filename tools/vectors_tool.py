from math import sqrt
import imaginary_tools as it

"""
python 3.11 based linear algebra calculator.
A more optimized version of the previous list_tools, using classes instead 
of lists of lists.
human readability is less emphasised in vectors_tool, 
so docstrings are generally shorter, except for child class definitions.
writing a C++ version
"""




def gen1d(l, u, splt, index):
    def splt_tr(func):
        def wrapper(*args, **kwargs):
            retl = []
            for i in range(0, splt):
                val = l + i*(l-u)/splt
                newargs = [j for j in args]
                newargs[index] = val
                retl.append(func(newargs, **kwargs))
            return retl
        return wrapper
    return splt_tr
"""
@gen1d(index=n) + @gen1d(index = m) = @gen2d(index1 = n, index2 = m)
"""
def gen2d(l1, u1, splt1, index1, index2, l2=None, u2=None, splt2=None):
    if l2 == None:
        l2, u2, splt2 = l1, u1, splt1
    def splt_tr(func):
        def wrapper(*args, **kwargs):
            retl = []
            for i in range(0, splt1):
                retl_i = []
                i_val = l1 + i*(u1-l1)/splt1
                for j in range(0, splt2):
                    j_val = l2 + j*(u2-l2)/splt2
                    arg_l  = [k for k in args]
                    arg_l[index1] = i_val
                    arg_l[index2] = j_val
                    retl_i.append(func(tuple(arg_l), kwargs))
                retl.append(retl_i)
            return retl
        return wrapper
    return splt_tr
                    
            

def input_vec_only(func):
    def wrapper(*args, **kwargs):
        args = (args[0], args[1].coord)
        result = func(*args, **kwargs)
        return result
    return wrapper

def string_check(func):
    def wrapper(*args, **kwargs):
        for i in args:
            if type(i) == str:
                raise TypeError("Error: cannot take string input")
        result = func(*args, **kwargs)
        return result
    return wrapper

def string_in_list_check(func):
    def wrapper(*args, **kwargs):
        for i in args:
            if type(i) == vector:
                continue
            else:
                try:
                    iterator = iter(i)
                except:
                    continue
                else:
                    for j in iterator:
                        if type(j) != (int or float):
                            raise TypeError("Error: iterable object only takes int or float input")
                        

def return_vec(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return vector(result)
    return wrapper

def conv_to_list(m1):
    return [i.coord for i in m1]

def proper_check(m1):
    row_length = len(m1[0])
    bool_list = [len(i) == row_length for i in m1]
    return bool_list

class vector():
    """
    vector class with basic operations for the gram schmidt calculator
    vector now used for all matrices
    .add() is redundant, for now, until matrix_operations includes addition
    """
    """
    vector confirmed to work 27/02/2024
    """
    def __init__(self, pos):
        """
        initialise with:
            
        a list representing the coordinates of the vector,
        
        the dimension of the list,
        
        a range object, for shorter comprehensions in multiple functions 
        iterating over each element of the vector
        """
        self.coord = pos
        self.dim = len(pos)
        self.iter8 = range(0, self.dim)
    def mod(self):
        """
        returns modulus of the vector and creates an attribute .moduli
        """
        size = 0 
        for i in self.iter8:
            size += self.coord[i]**2
        self.moduli = sqrt(size)
        return(self.moduli)
    

    def dot(self, vec2):
        """
        dot product of the vector with a user-input vector
        returns the dot product only
        """
        val=0
        for i in self.iter8:
            val+=self.coord[i]*vec2[i]
        return val
    
    def scalar(self, num):
        """
        scalar multiple of the vector
        returns only the value
        """
        return [num*self.coord[i] for i in  self.iter8]
    
    def add(self, vec2):
        return [self.coord[i]+vec2[i] for i in self.iter8]
    
    def subtract(self, vec2):
        x = [self.coord[i]-vec2[i] for i in self.iter8]
        return x
    
    def normalise(self):
        """
        divides each element of the list by the size of the vector
        """
        self.mod()
        n_list = self.scalar(1/self.moduli)
        self.norm = vector(n_list)
        return self.norm.coord


class matrix():
    
    def __init__(self, vecs):
        if not all(proper_check(vecs)):
            raise TypeError("cannot cast to matrix type, lengths non-uniform")
        self.vec = vecs
        self.rows = len(self.vec)
        self.cols = len(self.vec[0])
        self.veclist = [vector(vecs[i]) for i in range(0, self.rows)]
        self.square_mat = self.rows == self.cols
        self.orthogonalisable = not (self.rows>self.cols)
    def dimension(self):
        """
        returns tuple of dimension in Row Column form
        """
        return (self.rows, self.cols)
    def transpse(self):
        """
        returns transpose as a matrix class and assigns attribute self.transpose as a matrix class
        """
        tr = []
        for i in range(0, self.cols):
            trcol = [self.vec[j][i] for j in range(0, self.rows)]
            tr.append(trcol)
        self.transpose = matrix(tr)
        return self.transpose

    def sparseness(self):
        """
        creates boolean matrix which is True iff the corresponding matrix in self is 0
        returns the fraction of elements which are 0
        the higher the returned value /1, the more sparse the matrix.
        if square and sparseness index > 1/rows, det=0 (Nope)
        """
        s_mat = []
        for rows in self.vec:
            row_sparse = [i==0 for i in rows]
            s_mat.append(row_sparse)
        return (sum([sum(i) for i in s_mat])/(self.rows*self.cols))
    def make_square(self):
        """
        
        creates a class square_matrix, optimised for performing functions
        on square matrices, copies all attributes of the matrix class (super(). initiation)
        to call e.g. trace, use:
            self.square.trace()
        and the attribute trace is then:
            self.square.trace
        if it is already known that the matrix is square before defining
        as a matrix class, initialise using square_matrix instead of matrix,
        as this will avoid needing .square before every function,
        and also avoid confusion with the square of the matrix, which can
        only be defined for square matrices.
        """
        if self.square_mat:
            self.square = square_matrix(self.vec)
        else:
            raise ValueError("Could not convert matrix to class 'square_mat' - matrix not square")
    def gram_schmiidt(self):
        """
        creates class matrix_gramm, optimised for gram schmidt orthogonalisation \n
        call with self.gram.func/attribute. \n
        returns the list of vectors (classes) in the orthogonal basis. \n
        a human readable version is: \n
        self.gram.u_g_list \n
        g_sch() returns a non-normalised equivalent of u_g_sch(), 
        which can be called from self.gram \n
        """
        self.gram = matrix_gramm(self.vec)
        self.gram.u_g_list = self.gram.u_g_sch()
        return self.gram.unitmat
    
        
class square_matrix(matrix):
    """
    to add:
        
    matrix properties:
    inverses
    eigenvalues
    eigenvectors
    eigenspaces
    
    checks:
    invertible
    diagonalisable
    decomposable (for all corresponding decompositions, invertible is easy)
    
    decompositions:
    LU
    gauss jordan
    diagonalisation (eigenvectors/values)
    
    """
    def __init__(self, vecs):
        super().__init__(vecs)
        #as it's square, we could delete self.rows or self.cols, but they're just integers so not much point
        #del self.rows
        if not self.square_mat:
            raise TypeError("Could not cast to 'square_mat' - matrix not square")
    def trace(self):
        self.trce = sum([self.vec[i][i] for i in range(0, self.rows)])
        return self.trce
    def check_symmetric(self):
        sym_list = []
        for i in range(0, self.rows-1):
            for j in range(1, self.rows):
                sym_list.append(self.vec[i][j] == self.vec[j][i])
        self.is_symmetric = all(sym_list)
        return self.is_symmetric
    
    def transpose(self):
        if self.is_symmetric:
            return self
        else:
            tr = []
            x = self.cols
            for i in range(0, x):
                trcol = [self.vec[j][i] for j in range(0, x)]
                tr.append(trcol)
                self.transpose = square_matrix(tr)
                return self.transpose
    def EOF_ify(self):
#       #this took a while, so i'm going to keep improving it, 
        #so edit docstrings will be pretty large for now
        """
        iterate across the columns, and at each (ith) iteration of the nxn matrix:
            iterate down the n-i non-zerod elements of each column
            use the vector.add and vector.subtract and vector.scalar operations
            veclist gives a list of row vectors, with defined EROs
        """
        """
        things to add:
        in sparse matrices, there'll be a lot of zeros.
        it may be optimal to scan for large clusters of zeros (especially in a whole row)
        to speed this up, as m(n-1)^3 < n^3, especially when n is small?
        i.e. as runtime is n^3 but if m zeros are found in a row,
        there are only m (n-1)x(n-1) matrices to work with
        """
        for i in range(0, self.cols-1):
            for j in self.veclist[i+1].coord:
                scale = j
        useable_vecs = [self.veclist[0]]
        for i in range(1, self.cols):
            vec = self.veclist[i]
            for j in range(0, i):
                scale = vec.coord[j]/useable_vecs[j].coord[j]
                el_vector = useable_vecs[j].scalar(scale)
                vec = vector(vec.subtract(el_vector))
            useable_vecs.append(vec)
        EOF_mat = conv_to_list(useable_vecs)
        self.EOFd = matrix(EOF_mat)
        return self.EOFd
    def determinant(self):
        if self.cols == 2:
            x = self.vec
            det = x[0][0]*x[1][1]-x[0][1]*x[1][0]
        else:
            U_T = self.EOF_ify()
            U_T_list = U_T.vec
            det = 1
            for i in range(0, self.cols):
                det*=U_T_list[i][i]
        return det
    def two_d_case_eigenval(self):
        m = self.determinant()
        p = self.trace()
        disc = p**2 - 4*m
        if disc > 0:
            sol1 = (p + sqrt(disc))/2
            sol2 = (p - sqrt(disc))/2
            return (sol1, sol2)
        if disc == 0:
            return (p/2, p/2)
        if disc < 0:
            r = p/2
            c = sqrt(-disc)/2
            sol1 = it.imaginary(r, c)
            sol2 = it.imaginary(r, -c)
            return (sol1, sol2)
    def two_d_case_eigenvec(self):
        temp = self.vec
        λ = self.two_d_case_eigenval()
        a = temp[0][0]
        b = temp[0][1]
        c = temp[1][0]
        d = temp[1][1]
        if len(λ) == 2 and type(λ[0]) == float and λ[0] != λ[1]:
            v1 = vector([λ[0]-d, c])
            v2 = vector([b, λ[1]-a])
        elif len(λ) == 2 and type(λ[0]) == float and λ[0] == λ[1]:
            if b == c == 0:
                v1 = vector([1, 0])
                v2 = vector([0, 1])
            else:
                v1 = vector([λ[0]-d, c])
                v2 = vector([b, λ[1]-a])
        elif len(λ) == 2 and type(λ[0] == it.imaginary):
            v1 = []
            v2 = None
        return (v1, v2)
            
        
            
                


class matrix_gramm():
    """
    uses vector class to perform gram schmidt orthogonalisation and orthonormalisation
    input 2d lists as lists of vectors
    should work for any dimension
    
    as vector class is used, all functions of the vector class can be used.
    use self.veclist[i] to obtain the ith element of the list of vectors (which will be a vector class),
    then add .func() to perform the function
    i.e. self.veclist[i].mod() returns the moduli of the ith element,
    and assigns the moduli to an attribute self.veclist[i].moduli
    """
    def __init__(self, vecs):
        self.vec = vecs
        self.veclist = [vector(vecs[i]) for i in range(0, len(vecs))]
        self.rows = len(self.veclist)
    def gram_val(self, pos):
        """
        calculates the component of the nth vector (in the gram schmidt process)
        in the direction of the first n-1 vectors and subtracts this from the initial vector,
        calculating the nth vector of the basis of the gram schmidt process
        """

        ve = self.veclist[pos]
        we = self.veclist[pos]
        for i in range(0, pos):
            dot_g = ve.dot(g_list[i])
            g_cl = vector(g_list[i])
            mod_g = g_cl.mod()**2
            val = dot_g/mod_g
            scl_g_cl = g_cl.scalar(val)
            we = vector(we.subtract(scl_g_cl))
        return we
        
    def g_sch(self):
        """
        gram schmidt orthogonalisation, without normalisation,
        calculates gram_val for each element of the list veclist
        """
        global g_list
        g_list = [self.veclist[0].coord]
        for i in range(1, self.rows):
            v = self.gram_val(i)
            g_list.append(v.coord)
        return g_list
    def u_g_sch(self):
        """
        normalises the vectors of the gram schmidt process in gram_val
        using the .normalise() function in the vectors class
        """
        g_sch_mat = matrix_gramm(self.g_sch())
        u_g_list = [g_sch_mat.veclist[i].normalise() for i in range(0, self.rows)]
        self.unitmat = matrix_gramm(u_g_list)
        return u_g_list

class mat_operators():
    """
    class for methods between two matrices,
    includes:
    Left and Right multiplying
    to be added:
    multiplying one by the inverse of the other
    adding
    """
    def __init__(self, m1, m2):
        self.m1 = matrix(m1)
        self.m2 = matrix(m2)
        self.multiplicableL = len(m1[0]) == len(m2)
        self.multiplicableR = len(m2[0]) == len(m1)
        self.addable = self.m1.dimension() == self.m2.dimension()
    def multiplyL(self, error_return = True):
        if not self.multiplicableL:
            if error_return:
                raise ValueError("Could not multiply - types not of form n x m and m x p")
            else:
                return None
        self.m2.transpse()
        z = []
        for i in range(0, len(self.m1.vec)):
            x = []
            for j in range(0, len(self.m2.vec[0])):
                col_m2 = self.m2.transpose.vec[j]
                y = self.m1.veclist[i].dot(col_m2)
                x.append(y)
            z.append(x)
        self.multL = matrix(z)
        return self.multL
    def multiplyR(self, error_return = True):
        if not self.multiplicableR:
            if error_return:
                raise ValueError("Could not multiply - types not of form n x m and m x p")
            else:
                return None
        self.multR = mat_operators(self.m2.vec, self.m1.vec).multiplyL()
        return self.multR
    def add(self):
        if not self.addable:
            raise ValueError("Could not add - matrices not of same dimension")
        else:
            total = []
            for i in range(0, self.m1.cols):
                row_sum = self.m1.veclist[i].add(self.m2.vec[i])
                total.append(row_sum)
            self.total = matrix(total)
        return self.total
    def commute(self):
        self.commutative = (self.multiplyL().vec == self.multiplyR().vec)
        return self.commutative

class mat_vec():
    def __init__(self, m, v):
        self.m = m
        self.v = vector(v)
        self.eigenvals = []
        self.eigenvecs = []
    def multiply(self):
        mt = []
        for i in self.m:
            mt.append(self.v.dot(i))
        self.prod = mt
        self.check_eigen()
        return self.prod
    def check_eigen(self):
        if self.v.coord[0] == 0:
            pass
        else:
            ratio = self.prod[0]/self.v.coord[0]
            if all([self.prod[i] == ratio*self.v.coord[i] for i in range(1, len(self.v.coord))]):
                self.eigenvals.append(ratio)
                self.eigenvecs.append(self.v.coord)
        
    
    
