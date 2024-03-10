"""expanded form of the matrix section of list_tools"""

def convert_to_matrix(A, n):
    if len(A)%n != 0:
        print("A cannot be broken up into n rows")
        return 
    return_list = []
    for i in range(0, len(A)//n):
        intermed_list = []
        for j in range(0, n):
            intermed_list.append(A[i*n+j])
        return_list.append(intermed_list)
    return return_list

#O(n) = A, but appending to a list can be quick so this shouldn't bottleneck anything
def convert_matrix_to_list(A):
    returnlist= []
    for i in A:
        for j in i:
            returnlist.append(j)
    return returnlist


def is_empty(A):
    return len(A)==0

def size_of_matrix(A):
    if len(A) == 0:
        return 0
    return len(A)*len(A[0])

def is_square(A):
    if len(A)==0:
        return False
    size_A = size_of_matrix(A)
    if float(int(size_A**0.5)) == size_A**0.5:
        return len(A) == int(size_A**0.5)

def all_values_zero(A):
    checklist = []
    for i in A:
        checklist_j = []
        for j in i:
            checklist_j.append(j==0)
        checklist.append(all(checklist_j))
    return all(checklist)

def all_values_equal(A):
    checklist = []
    for i in A:
        checklist.append(min(i) == max(i))
    return all(checklist)

def all_values_equalto(A, *, n=0):
    checklist = []
    for i in A:
        checklist_j = []
        for j in i:
            checklist_j.append(j==n)
        checklist.append(all(checklist_j))
    return all(checklist)

def same_size(A, B):
    A_0 = len(A)==0
    B_0 = len(B)==0
    if A_0 or B_0:
        return (A_0 and B_0)
    return len(A)*len(A[0]) <= len(B)*len(B[0])

#O(n) = min(A, B)
"""NOTE: while in proper matrix algebra, only matrices of equal size can be added,
The code will run for matrices of non-equal size where one is smaller than the 
other by both rows and columns if require_equal_size is set to False, by 
adding top left elements of each together and working from the top left.
The code will blow up if one matrix has more rows than the other, and the other 
has more columns than the first.

require_equal_size is set to True by default, as a non-required keyword argument,
but can optionally be given in the function definition.
"""

def add_matrices(A, B, *, require_equal_size = True):
    if require_equal_size and (len(A) != len(B) or len(A[0]) != len(B[0])):
        print("require matrices same size set to true and matrices were not same size")
        return
    A_smallest = len(A)*len(A[0]) <= len(B)*len(B[0])
    if A_smallest:
        for i in A:
            for j in A:
                B[i][j]+=A[i][j]
        return B
    else:
        for i in B:
            for j in B:
                A[i][j]+=B[i][j]
        return A


def are_multiplicable(A, B):
    return len(A[0])==len(B)

def get_column_n(A, n):
    return_list = []
    for i in A:
        return_list.append(i[n])
    return return_list
    
    
#O(n) = A*number of rows of A = (number of rows of A)^2 * number of columns of A
#O(n) roughly equal to A^(3/2) or number of rows^3 assuming roughly square matrix
def multiply_matrices(A, B, *, require_equal_size = False):
    if require_equal_size and (len(A) != len(B) or len(A[0]) != len(B[0])):
        print("require matrices same size set to true and matrices were not same size")
        return
    if not are_multiplicable(A, B):
        print("matrices cannot be multiplied as rows of A is not equal to columns of B")
        return
    else:
        return_list = []
        for i in range(0, len(A)):
            return_row = []
            for j in range(0, len(A)):
                runn_total = 0
                row = A[i]
                col_B = get_column_n(B, j)
                for k in range(0, len(row)):
                    runn_total+=row[k]*col_B[k]
                return_row.append(runn_total)
            return_list.append(return_row)
    return return_list

def transpose(A):
    if len(A) == 0:
        return []
    mtlist = []
    for i in range(0, len(A[0])):
        mtlist.append([A[j][i] for j in range(0, len(A))])
    return mtlist

#works by repeated recursion, VERY slow, VERY memory intensive
def get_det_slow(A):
    if not is_square(A):
        print("could not calculate determinant: matrix is not square")
        return
    if is_empty(A):
        return 0
    if len(A) == 1:
        return A[0]
    if len(A) == 2:
        det = A[0][0]*A[1][1] - A[0][1]*A[1][0]
        return det
    det = 0
    for i in range(0, len(A)):
        col = get_column_n(A, i)
        B = A.remove(col)
        B = B.remove(A[i])
        det+=i*get_det_slow(B)