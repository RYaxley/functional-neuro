% function output = voxeltest(X,Y,Z)
%   TESTVOXEL   Short description
%       [OUTPUT] = TESTVOXEL()
% 
%   Long description
%   
%   Created by Richard Yaxley on 2008-06-04.

         
% 1. Turn off the annoying warning messages.
warning off all
                  
% 2. Set the base directory of the experiment according to the platform we are on.
if ispc
    EXPERIMENT = findexp('CUD.01');
elseif isunix
    EXPERIMENT = fullfile('~/','CUD.01');
end

% 3. Set the directory of the model we are currently working on.
MODEL='Model.9';

% 4. Set the directory path for reading in the behavioral data.
IPATH = fullfile(EXPERIMENT,'Analysis',MODEL,'Outcome','Level.1'); % Set data path

% 6. Set the year of the data we want to process. 
SUBYEAR='200';

% 7. Create a list of subjects that exist in the 'input' directory.      
SUBJECTS = find_subjects(IPATH,SUBYEAR);

% for s = 1:length(SUBJECTS) 
      
% Specify current Subject ID
ID = SUBJECTS{12}
RUN = 'run01.feat';	    
 
% Go to data directory and read in the 'design.mat' file
cd(fullfile(IPATH,ID,RUN)); 
fid = fopen('design.mat','r');
fscanf(fid,'%s',1); % Omit unnecessary text from beginning of file
NumWaves = fscanf(fid,'%f',1); % Read in number of waveforms
fscanf(fid,'%s',1); % Omit unnecessary text
NumPoints = fscanf(fid,'%f',1); % Read in number of time points
fscanf(fid,'%s',NumWaves+2); % Omit unnecessary text          
  
design = [];   

% Read in all of the parameter estimates
for Point = 1:NumPoints
    for Wave = 1:NumWaves
        design(Point,Wave) = fscanf(fid,'%f',1); 
    end
end
                
fid(close); % 'design.mat'

                                                        
% Open Filtered Func data
% func = readmr('filtered_func_data.nii.gz','NOPROGRESSBAR'); 

% Select data from func for one voxel over time
% voxel = func.data(22,22,23,:);
% voxel = func.data(X,Y,Z,:); 
voxel = func.data(37,32,22,:);
  

% Reduce 4-D voxel data to vector
y = [];
y(:,1) = voxel(1,1,1,:);    
          
% General Linear Model
[B,DEV,STATS] = glmfit(design(:,[1,3:8]),y,'normal');  
disp('Original model') 
disp Betas
disp(B(2:3))   
disp p-values                     
disp(STATS.p(2:3))
              
% Get rid of Motion Parameters
design_nomotion = design(:,1);   
[B,DEV,STATS] = glmfit(design_nomotion,y,'normal');        
disp('No Motion Parameters')
disp Betas
disp(B(2))   
disp p-values                     
disp(STATS.p(2))
                           
% Muck with variables to push around results with randomized IVs      
design_random = design; %(:,1:2);
% design_random(:,1) = design_random(:,1).*randperm(length(design))';   
design_random(:,1) = design(randperm(length(design)),1);
[B,DEV,STATS] = glmfit(design_random,y,'normal');
disp('Randomized')
disp Betas
disp(B(2:3))   
disp p-values                     
disp(STATS.p(2:3))  

% Muck with variables to push around results with randomized IVs      
design_random_nomotion = design_random(:,1:2);
[B,DEV,STATS] = glmfit(design_random_nomotion,y,'normal');
disp('Randomized without Motion Parameters')
disp Betas
disp(B(2:3))   
disp p-values                     
disp(STATS.p(2:3))
                   

% end % Subject loop

% end %  function