 %%% Compression %%%
S=1000; %en mm²
F=534; %en N (obtenu grâce au cas de charge : BJ_front tie rod inboard)

Contrainte_comp=F/S

 %%% Compression %%%
 
r=3; %en mm (rayon de vis)
S_vis=pi*r^2; %en mm²

Contrainte_traction=F/S_vis

%En traction la contrainte est insignifiante vis-à-vis de la limite
%élastique de l'aluminium (environ 260MPa)
%En compression la contrainte est de 18MPa pour une contrainte max
%admissible de 640MPa ce qui est largement sur dimensionné. 
