curPath=pwd;
path_libs=[curPath,'\asw_libs'];
addpath(genpath(path_libs),'-begin');
    
Path_m_temp=[curPath,'\DT_E_C_m'];
fp=findfiles(Path_m_temp,'m');
nump=size(fp,1);
for i=1:1:nump
   run(fp{i,1});
   disp('......');
   disp(fp{i,1});
end





clear Path_m_temp;
    
    

    
    