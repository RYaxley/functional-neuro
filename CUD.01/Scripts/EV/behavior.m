% function behav2stats2;

% Set the base directory of the experiment
if ispc
    exp = findexp('CUD.01');
elseif isunix
    exp = fullfile('~','CUD.01');
end

% Set the directory path for reading in the behavioral data.
ipath = fullfile(exp,'Analysis','Behavioral','!Overall');

% Read data files for each group. These data include the mean RTs for each condition.
data = [];
group = {'adults1','adults2','controls'};

for i = 1:length(group)

	fid = fullfile(ipath,[group{i} '.mat']);
	if exist(fid,'file')==2
		load(fid)
	end

	data = sub_data;
		
end

% Group Descriptives
groups = vertcat(data(:,1),data(:,1),data(:,1));
% Collapse Adults1 and Adults2 to single group
a2idx = find(groups==2);
groups(a2idx)=1;

% Conditions (1=No risk, 2=Reward risk, 3=Behavioral risk)
c = ones(length(data(:,1)),1);
condition = vertcat(c,c*2,c*3);

% Create a single column of RTs
rt = reshape(data(:,4:6),[],1);

data

% Create a single column of RTs
s = data(:,2);
s = vertcat(s,s,s);

disp('Overall')
[m,sd] = grpstats(rt,[],{'mean','std'});

disp('Group')
[m,sd] = grpstats(rt,{groups},{'mean','std'});

disp('Condition')
[m,sd] = grpstats(rt,{condition},{'mean','std'});

disp('Group X Condition')
[g,m,sd,ci]  = grpstats(rt,{groups,condition},{'gname','mean','std','predci'})

% Two-way ANOVA to compare mean RTs for 2 (Groups) X 3 (Condition)
[p,table,stats] = anovan( ...
				  rt, 			     ... % Dependent response variable
				  {groups,condition}, ... % Predictor variables
				  'model','full',    ... % Model type
				  'display','off',   ... % Display table
				  'varnames',strvcat('Group','Risk') ...
				  )
			
% Display a reduced version of the ANOVA output  
disp('ANOVA - RT')
table(1:4,[1 6 7])

Y = rt;
S = s;
F1 = groups;
F2 = condition;
FACTNAMES = {'group', 'cond'}
stats = rm_anova2(Y,S,F1,F2,FACTNAMES)



%    % Figures
%    figure     
Y = m % Response variable
%    E = SE'; % Standard error    
%    width = [];
%    conds = {'None'; 'Reward'; 'Behavioral'};
%    title = ROI;    
%    xlabel = 'Types of Risk';
%    ylabel = '% Signal Change';
%    color = 'gray';
%    grid = 'none';
%    legend = {'Adults'; 'Adolescents'};
%    barweb(Y, E, width, conds, title, xlabel, ylabel, color, grid, legend);



z = struct('rt',rt,'sub',s,'group',groups,'cond',condition)
% figure out how to write struct to csv? to open in jmp
fid = fopen('output.txt','w')
fprintf(fid,'RT\tSUB\tGRP\tCOND\n')
% fprintf(fid,'[%5.0d] [%5.10f] [%5.5f] [%5.5f] \n',S,Y,F1,F2)
% fprintf('%5.0d\t%5.5f\n',S,Y)
%for i = 1:numel(z.rt)
%	fprintf(fid,'%5.3d\t%5.5f\n',z(i).rt,z(i).sub);
%end
fclose(fid)

d = {z}
fid = 'output.xls'
xlswrite(fid,z.rt,'rt')

% % t-Test to compare mean RTs between 2 groups
% disp('t-test - RT')
% [h,p,ci,stats] = ttest2(data(group1,4:6),data(group2,4:6))
