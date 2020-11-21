import networkx as nx
import random
from subprocess import Popen, PIPE
import numpy as np
from sympy import Poly
from sympy.abc import x


def get_FQ(N, types = 'F'):
    p = Popen(['char_struct.exe'], shell=True, stdout=PIPE, stdin=PIPE)
    def wri_ex(val, getres = False):
        val = str(val) + '\n'
        val = bytes(val, 'utf8')
        p.stdin.write(val)
        p.stdin.flush()
        if getres:
            result = p.stdout.read().strip().decode("utf-8")
            result = str(result).split('\n')
            #print(result)
            ans = []
            for vals in result:
                a1, a2 = vals.split('!')
                a1, a2 = int(a1), int(a2)
                ans.append(a1 if abs(a1) < abs(a2) else a2)
            return ans
    n = N
    wri_ex(n)
    G = nx.path_graph(n)
    L = nx.linalg.laplacian_matrix(G).toarray()
    L = list(L)
    #print(L)
    if types != 'F':
        L[n-1][n-1] = 0
        L[n-2][n-1] = 0

    for ii in range(n):
        for jj in range(n):
            
            if ii == n-1 and jj == n-1:
                break
            wri_ex(L[ii][jj])
    pols = wri_ex(L[n-1][n-1], getres = True)
    pols.reverse()
    return Poly(pols, x, domain = 'ZZ')



if __name__ == "__main__":
    n = 2
    Fnm1 = get_FQ(n, types = 'F')
    Qnm1 = get_FQ(n, types = 'Q')
    Fnq = Fnm1*(1 - x) + Qnm1
    Fn = get_FQ(n + 1, types = 'F')
    print(Fnq, Fn)

    
    Qnq = Fnm1 * (-x) + Qnm1
    Qn = get_FQ(n + 1, types = 'Q')
    print(Qn, Qnq)    