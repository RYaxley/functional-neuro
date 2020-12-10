%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Script: 	
%
% Project: 	CUD.01
% Author: 	Richard Yaxley       
% Updated: 	May 16, 2008
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
      
% 1. Turn off the annoying warning messages.
warning off all
                  
% 2. Set the base directory of the experiment according to the platform we are on.
if ispc
    EXPERIMENT = findexp('CUD.01');
elseif isunix
    EXPERIMENT = fullfile('~/','CUD.01');
end

% 3. Set the directory of the model we are currently working on.
MODEL='Model.8';

% 4. Set the directory path for reading in the behavioral data.
% IPATH = fullfile(EXPERIMENT,'Analysis',MODEL,'Level.2'); % Set data path
IPATH = fullfile(EXPERIMENT,'Analysis',MODEL,'Outcome','Decision+Reward','Level.2'); % Set data path

% 6. Set the year of the data we want to process. 
SUBYEAR='200';

% 7. Create a list of subjects that exist in the 'input' directory.      
SUBJECTS = find_subjects(IPATH,SUBYEAR);

for s = 1:length(SUBJECTS) 
      
 	% Specify current Subject ID
	ID = SUBJECTS{s};  
	
	% Specify the name of the data file to open and then open it.     
	TEMPDIR = pwd;             
    % cd(fullfile(IPATH,ID,'2.level.gfeat','cope19.feat','stats')) 
	cd(fullfile(IPATH,ID,'2.level.gfeat','cope5.feat','stats'))        
	pwd
	TEMPIMG = readmr('zstat1.nii.gz','NOPROGRESSBAR');
	cd(TEMPDIR)        
	 
	try 
		exist DATA;     
		IMG(:,:,:,end+1) = TEMPIMG.data;
	catch
		IMG = NaN(0,0,0,0);       
		IMG(:,:,:,end+1) = TEMPIMG.data;       
	end                                    
	
end % Subject loop                           

showsrs2(IMG)