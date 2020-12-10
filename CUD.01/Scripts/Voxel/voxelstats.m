function voxelstats(subj,run,ntimepoints,nPs,time,copes,outputdirname) %subj and run are strings

datadir=['S:\Analysis\Cluster\PassiveTask\' subj '\' subj '_FEAT_noTD_6mm_ST_v0.6.5\' subj '_run' run '_noTD_crap_removed.feat']
cd(datadir)


fid = fopen('design.mat','r');
fscanf(fid,'%s',12);
designmatrix=[];
for t=1:ntimepoints
    for p=1:nPs
        designmatrix(t,p)=fscanf(fid,'%f',1);
    end
end
fclose(fid);
filtdatadir=['S:\Analysis\Cluster\PassiveTask\' subj '\PrestatsOnly\' subj '_prestats6mm_ST\' subj '_prestatsonly' run '.feat'];
cd(filtdatadir) 
data=readmr('masked_filtered_func_data.nii','NOPROGRESSBAR');
cd(datadir)
mask=readmr('mask.nii.gz','NOPROGRESSBAR');

cd stats
copefile=readmr('pe1.nii.gz','NOPROGRESSBAR');
cd ..

for PE=1:nPs
    eval(['PEimage' num2str(PE) '=copefile;'])
end


datasize=size(mask.data);
for x=1:datasize(1)
    for y=1:datasize(2)
        for z=1:datasize(3)
            if mask.data(x,y,z)==1
                voxel=data.data(x,y,z,:);
                timelength=length(voxel);
                newvoxel=reshape(voxel,timelength,1);
                eval(['newvoxel2=newvoxel(' time ');'])
                eval(['designmatrix2=designmatrix(' time ',' copes ');'])
                [b,dev,stats]=glmfit(designmatrix2,newvoxel2,'normal');
                copevector=str2num(copes);
                for PEx=1:length(copevector)
                    PE=copevector(PEx);
                    PE_new=PE+1;
                    eval(['PEimage' num2str(PE) '.data(x,y,z)=stats.beta(' num2str(PE_new) ');'])
                end
            else
                copevector=str2num(copes);
                for PEx=1:length(copevector)
                    eval(['PEimage' num2str(PEx) '.data(x,y,z)=0;'])
                end
            end
        end
    end
end


mkdir(outputdirname)
cd(outputdirname)
for PEx=1:length(copevector)
    PE=copevector(PEx);
    PE_new=PE+1;
    eval(['writemr(PEimage' num2str(PE) ',''PE' num2str(PE) 'image.bxh'',''BXH'')']);
    bxh2analyze_cmd=['bxh2analyze -s -b --niigz PE' num2str(PE) 'image.bxh PE' num2str(PE) ];
    system(bxh2analyze_cmd);
    file1=['PE' num2str(PE) 'image.bxh'];
    file2=['PE' num2str(PE) 'image.data'];
    delete(file1);
    delete(file2);
end


