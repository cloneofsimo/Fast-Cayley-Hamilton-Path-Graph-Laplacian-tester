from sympy import Poly
from sympy.abc import x
import sympy


g_zeros = [1, 2, 3, 5, 1]
f_zeros = [5, 6, 22, 11, 2]

p = int(1e9) + 7

def invs(x):
    return pow(x + p, p-2, p)

#find resultant first:
ans = 1
for gs in g_zeros:
    for fs in f_zeros:
        ans = ans * (gs + fs)
       
print(ans%p)

#find resultant by reductions:

g_pol = Poly(1, x, modulus = p)
f_pol = Poly(1, x, modulus = p)
for gs in g_zeros:
    g_pol = g_pol * (gs - x)

for fs in f_zeros:
    f_pol = f_pol *(fs - x)

pp = [p] * 100
pp = Poly(pp, x)
#print(pp)

def tru_mod(P):
    pc = P.all_coeffs()
    pc = [(a + p)%p for a in pc]
    return Poly(pc, x, modulus = p)


def reduction(P, Q):
    P = tru_mod(P)
    pc = P.coeffs()
    Q = tru_mod(Q)
    qc = Q.coeffs()
    
     #return Q, P - Q*ux^r    
    I = invs(qc[0])
    c = len(pc) - len(qc)
    subs = pc[0]*I*Q*(x**c)
    subs = Poly(subs, modulus = p)
    R = P - subs + p
    return Q, Poly(R, modulus = p)

def resultant(F, G, res):
    
    F, G = tru_mod(F), tru_mod(G)
    
    
    print(F, G)
    if F.degree() == 1 and G.degree() == 1:
        return F, G, res
    
    Gs = G.subs(x, -x)
    Gs = Poly(Gs + pp, x, modulus = p)
    
    A, R = reduction(F, Gs)
    res = res * pow(R.coeffs()[0], G.degree(), p) % p
    res = -res if R.degree() % 2 else res
    R = tru_mod(invs(R.coeffs()[0]) * R)
    R = -R if R.degree() % 2 else R
    
    return resultant(G, R, res)

anss = 1
for gs in g_zeros:
    anss *= f_pol.eval(x, -gs)

anss = 1
for fs in f_zeros:
    anss *= g_pol.eval(x, -fs)

# 나눠:

_, r_pol = reduction(f_pol, Poly(g_pol.subs(x, -x), x))
anss = 1
print(r_pol)
for gs in g_zeros:
    anss *= r_pol.eval(-gs)

print(anss)


f, g, res = resultant(f_pol, g_pol, 1)
'''
f = invs(f.coeffs()[0])*f
f = Poly(f + pp, x, modulus = p)
g = invs(g.coeffs()[0])*g
g = Poly(g + pp, x, modulus = p)
'''
print(f, g, res)
print((f.coeffs()[1] + g.coeffs()[1])*res %p)
