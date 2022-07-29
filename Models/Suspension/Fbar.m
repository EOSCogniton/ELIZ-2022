function [Accel_f,Accel_r] = Fbar(lf,lr,m,mur,muf,ms,rep,D_roue,Tr,Tf,Kr,Kf,h_g,g,coeff_adh)
af=1;
C=m*af*g*(h_g-D_roue/2);
Wfstat=0.5*g*(mur+ms*(1-rep));
DWuf=af*g*muf*D_roue/2/Tf;
DWsff=ms*af*g*(1-rep)*h_g/Tf;
Kphir=Tr^2*Kr+2*lr;
Kphif=Tf^2*Kf+2*lf;
DWscf=Kphir/(Kphif+Kphir)*C/Tf;
Wf=Wfstat+DWsff+DWuf+DWscf;
while coeff_adh*Wf>=m*af*g*(1-rep)
    C=m*af*g*(h_g-D_roue/2);
    DWuf=af*g*muf*D_roue/2/Tf;
    DWsff=ms*af*g*(1-rep)*h_g/Tf;
    DWscf=Kphir/(Kphif+Kphir)*C/Tf;
    Wf=Wfstat+DWsff+DWuf+DWscf;
    af=af+0.00001;
end

ar=1;
C=m*ar*g*(h_g-D_roue/2);
Wfstat=0.5*g*(mur+ms*rep);
DWur=ar*g*muf*D_roue/2/Tr;
DWsfr=ms*ar*g*rep*h_g/Tr;
DWscr=Kphif/(Kphif+Kphir)*C/Tr;
Wf=Wfstat+DWsfr+DWur+DWscr;
while coeff_adh*Wf>=m*ar*g*rep
    C=m*ar*g*(h_g-D_roue/2);
    DWur=ar*g*muf*D_roue/2/Tr;
    DWsfr=ms*ar*g*rep*h_g/Tr;
    DWscr=Kphif/(Kphif+Kphir)*C/Tr;
    Wf=Wfstat+DWsfr+DWur+DWscr;
    ar=ar+0.00001;
end



Accel_f = af;
Accel_r = ar;
end

