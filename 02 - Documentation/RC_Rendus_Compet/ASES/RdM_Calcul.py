#Calculs ASES

import math
def bending_rectangular():
    a  = 0.321
    b = 0.356
    e = 0.002
    I = e*b**3/12
    n = 4
    q = n *2.6*20*9.8/(a*b)
    m = 70
    #q = 40* m * 9.8
    Mmax = 0.0264*q*a**2
    Sigma_max = Mmax*e/(2*I)
    print("a(m) = ", a)
    print("b(m) = ", b)
    print("e(m) = ", e)
    #print("m_TSAC(kg)" , 70)
    print("n = ", n)
    print("q (Pa) = ", q)
    print("M_max (Nm) = ",Mmax)
    print("sigma_max (MPa) = ", Sigma_max/10**6)
    print("sigma_e (MPa) =", 300)

bending_rectangular()

def bending_circular():
    a = 0.0092
    b = 0.007014
    h = 0.0008
    m_cell = 0.040
    k = 0.105
    q = 20*9.8*m_cell/(3.14*(a**2 - b**2))
    smax = k * q * a**2/(h**2)
    print("a(m) = ", a)
    print("b(m) = ", b)
    print("h(m) = ", h)
    print("q (Pa) = ", q)
    print("sigma_max (MPa) = ", smax/10**6)
    print("sigma_e (MPa) =", 30)


"""

def buckling()
    a=0.452
    b=0.360
    e= 0.002
    mu = 0.3
    E = 210*10**9
    m = 35
    phi = a/b
    K = 1/phi**2 +phi**2 + 2
    pi = math.pi
    sigma_Cr = K * math.pi**2 * E /(12*(1-mu**2))*(e/b)**2
    S = b*e
    F_cr = sigma_Cr * S
    q = 20*9.8*m/(b*e)

    print("a(m) = ", a)
    print("b(m) = ", b)
    print("e(m) = ", e)
    print("m_TSAC(kg)", 70)
    print("E (GPa) = ", 210)
    print("sigma_cr (MPa) = ", sigma_Cr/10**6)
    print("q (MPa) =", q/10**6)

"""