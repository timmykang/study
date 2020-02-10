def babai(A, w):
    ''' http://sage-support.narkive.com/HLuYldXC/closest-vector-from-a-lattice '''
    C = max(max(row) for row in A.rows())
    B = matrix([list(row) + [0] for row in A.rows()] + [list(w) + [C]])
    B = B.LLL(delta=0.9)
    return w - vector(B.rows()[-1][:-1])