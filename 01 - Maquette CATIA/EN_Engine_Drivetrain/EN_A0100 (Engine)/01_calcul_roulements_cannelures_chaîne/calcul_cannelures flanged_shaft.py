
import numpy as np
import matplotlib.pyplot as plt
from math import pi
from scipy.optimize import fsolve, fmin, curve_fit
from scipy.interpolate import RegularGridInterpolator

#%% Materiau

Re=850*10**6
p_matage=80*10**6

#%% Calcul cannelures flancs en développantes

C=240

def inv(x):
    return np.tan(x)-x


def stress(m,Z,gw):
    alpha=20*pi/180
    
    esv=100*10**(-6)
    
    D=m*Z
    DB=D*np.cos(alpha)
    
    DEE=m*(Z+1.8)
    DEI=m*(Z+2)
    DII=m*Z
    DIE=m*(Z-0.4)
    
    
    E=pi*m/2
    alphai=np.arccos(DB/DEE)
    wi=DEE*(E/D+inv(alpha)-inv(alphai))
    ti=pi*DEE/Z-wi
    tau_m=2*C/DB*1/(Z*gw)*1/ti
    
    S=pi*m/2
    alphaj=np.arccos(DB/DII)
    wj=DEE*(S/D+inv(alpha)-inv(alphaj))
    tj=pi*DEE/Z-wj
    tau_a= 2*C/DB*1/(Z*gw)*1/tj
    
    sigma=8*C/(Z*gw)*1/(DEE**2-DII**2)
    
    return [sigma,tau_m,tau_a]

def von_mises(sigma,tau_x,tau_y):
    return (sigma**2+3*(tau_x+tau_y)**2)**(1/2)



list_m=np.array([1,1.25,1.5,1.667])*0.001
list_z=np.array(range(8,25))
GW=0.02

plt.figure(1)

plt.clf()

for m in list_m:
    m_label= 'm = ' + str(m*1000) + ' mm'
    s=stress(m,list_z,GW)
    vm=von_mises(s[0],s[1],s[2])/10**6
    plt.plot(list_z,vm,'.',label=m_label)
plt.ylabel('Contrainte de Von Mises (MPa)')
plt.xlabel('Nombre de dents')
plt.grid(True)
plt.legend()

plt.figure(2)

plt.clf()

for m in list_m:
    m_label= 'm = ' + str(m*1000) + ' mm'
    s=stress(m,list_z,GW)
    vm=von_mises(s[0],s[1],s[2])
    plt.plot(list_z,Re/vm,'.',label=m_label)
plt.ylabel('Coeff de sécurité / déformation plastique')
plt.xlabel('Nombre de dents')
plt.grid(True)
plt.legend()

plt.figure(3)

plt.clf()

for m in list_m:
    m_label= 'm = ' + str(m*1000) + ' mm'
    s=stress(m,list_z,GW)[0]
    plt.plot(list_z,p_matage/s,'.',label=m_label)
plt.ylabel('Coeff de sécurité / matage')
plt.xlabel('Nombre de dents')
plt.grid(True)
plt.legend()


