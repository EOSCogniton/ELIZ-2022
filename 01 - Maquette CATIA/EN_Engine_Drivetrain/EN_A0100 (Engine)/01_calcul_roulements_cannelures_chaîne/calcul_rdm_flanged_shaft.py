from math import pi
import numpy as np
import matplotlib.pyplot as plt


#%% Calcul concentration de contrainte dans la gorge de l'arbre

Re=850*10**6    

C=240 #couple moteur

T=7240 #traction de la chaîne
l=16.45 #bras de levier entre point d'application de la traction et gorge (mm)



#concentration de conrainte arbre avec gorge c.f.

def K_flex(D,d,r,t):
    kp=(t/r*d/D/(1-d/D)+1)**(1/2)-1
    kq=(t/r)**(1/2)
    return 1+1/(1/(0.715*kp)**2+1/(2*kq)**2)**(1/2)

def K_tor(D,d,r,t):
    kp=(t/r*d/D/(1-d/D)+1)**(1/2)-1
    kq=(t/r)**(1/2)
    return 1+1/(1/(0.366*kp)**2+1/kq**2)**(1/2)
    

def von_mises(T,l,D,r):
    
    d=D-2*r
    Mf=T*l
    sigma=Mf*32/(pi*d**3)
    Kf=K_flex(D,D-2*r,r,r)
    
    Mt=C
    tau=16*Mt/(pi*d**3)
    Kt=K_tor(D,D-2*r,r,r)
    
    return ((Kf*sigma)**2+3*(Kt*tau)**2)**(1/2)
    

#print('sigma_VM=',round(VM/1000000),'MPa')
#print('coefficient de sécurité',round(Re/VM*100)/100)

t1='Contrainte en MPa pour une tension de '+str(round(T/1000*100)/100)+' kN et un bras de levier de '+str(round(10*l)/10)+' mm'
t2='Coefficient de sécurité pour une tension de '+str(round(T/1000*100)/100)+' kN et un bras de levier de '+str(round(10*l)/10)+' mm'

list_r=np.linspace(1.5,2.5,50)/1000
list_D=np.linspace(15,30,50)/1000

mesh_r,mesh_D=np.meshgrid(list_r, list_D)

VM=von_mises(T,l/1000,mesh_D,mesh_r)

plt.figure(1)
plt.clf()
cont=plt.contour(mesh_r*1000, mesh_D*1000, VM/10**6,10)
plt.clabel(cont)
plt.xlabel('rayon de gorge (mm)')
plt.ylabel('diamètre extérieur (mm)')
plt.title(t1)
plt.grid(True)

plt.figure(2)
plt.clf()
cont=plt.contour(mesh_r*1000, mesh_D*1000, Re/VM,10)
plt.clabel(cont)
plt.xlabel('rayon de gorge (mm)')
plt.ylabel('diamètre extérieur (mm)')
plt.title(t2)
plt.grid(True)

plt.show()
