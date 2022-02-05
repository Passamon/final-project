from re import S
from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt

def odes(x, t):
    # constants
    beta = 1.18e-9
    zetas = 0.0002
    zetah = 0.00015
    omega1=0.0083
    omega2=0.0058
    omega3=0.00135
    epsilon1=0.641
    epsilon2=0.704
    mu=3.6529e-5
    alpha=0.013
    lambdas=0.02
    lambdah=0.012


    # assign each ODE to a vector element
    # S = x[0]
    # I = x[1]
    # V1 = x[2]
    # V2 = x[3]
    # M = x[4]
    # H = x[5]
    # R = x[6]
    # D = x[7]

    S = x[0];
    V1 = x[1];
    V2 = x[2];
    I = x[3];
    R = x[4];
    H = x[5];
    M = x[6];

    # define each ODE
    dSdt = - beta*S*I - omega1*S - mu*S
    dV1dt = omega1*S - omega2*V1 - beta*(1-epsilon1)*V1*I - mu*V1
    dV2dt = omega2*V1 - omega3*V2 - beta*(1-epsilon2)*V2*I - mu*V2
    dMdt = omega3*V2 + R - beta*(1-epsilon2)*M*I - mu*M
    dIdt = beta*S*I + beta*(1-epsilon1)*V1*I + beta*(1-epsilon2)*V2*I + beta*(1-epsilon2)*M*I - alpha*I -lambdas*I - zetas*I
    dHdt = alpha*I - lambdah*I - zetah*H
    dRdt = lambdas*I + lambdah*H -R
    dDdt = zetas*I +zetah*H

    return[dSdt,dV1dt,dV2dt,dIdt,dRdt,dHdt,dMdt,dDdt]



# innitial conditions
N = 66186000
print(N)
x0=[51001012,13955087,3911439,615314,13402,205002,405322,4990]


t = np.linspace(0,14,15)
x = odeint(odes,x0,t)
print(x)

# S = x[:,0]
# I = x[:,1]
# V1 = x[:,2]
# V2 = x[:,3]
# M = x[:,4]
# H = x[:,5]
# R = x[:,6]
# D = x[:,7]



# plt.semilogy(t,S)
# plt.semilogy(t,I)
# plt.semilogy(t,V1)
# plt.semilogy(t,V2)
# plt.semilogy(t,M)
# plt.semilogy(t,H)
# plt.semilogy(t,R)
# plt.semilogy(t,D)
# plt.show()