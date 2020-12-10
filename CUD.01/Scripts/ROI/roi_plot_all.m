%function roi_plot(EXP,MODEL,REGIONS)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%   roi_plot   organizes featquery data
%
%       example: roi_plot('CUD.01','Decision.B-CR','200')
%
%   Reads in and organizes FeatQuery data. Also, performs initial
%   statistical tests.
%
%   Created by Richard Yaxley
%   Updated on September 30, 2008
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Set the base directory of the experiment according to the platform we are on.

EXP='CUD.01';
MODEL='Decision';
if ispc
    EXPERIMENT = findexp(EXP);
elseif ismac
    EXPERIMENT = fullfile('/Volumes',EXP);
end

% Set the directory path for reading in the behavioral data.
IPATH = fullfile(EXPERIMENT,'Analysis',MODEL,'ROI');

% Set the output path for our processed ROI data.
OPATH  = fullfile(IPATH,'!Output');
try
    mkdir(OPATH); % Create output directory if it doesn't exist
end

% Create a list of subjects that exist in the 'input' directory.
%SUBYEAR='3';
%SUBJECTS = find_subjects(IPATH,SUBYEAR);
%length(SUBJECTS)

% Set the EV numbers corresponding to C, RR, and BR COPES
COPES = [1,3,5];

% Set the regions-of-interest to process (excluding filename suffix)
REGIONS = { 'pcc2' }
titles = {'PCC'};


% MUST REDO THIS

% get_subjects
%
% groupscell= num2cell(groups)
%
% % Set a vector to identify the two groups (eg, Adults = 1, Kids = 2)
% GROUP1 = '1';
% GROUP2 = '2';
% GROUP2 = '3';
%
% %[hits] = regexp(SUBJECTS,GROUP1,'match');
% [hits] = regexp(groupscell,GROUP1,'match')
%
% for i = 1:length(hits)
%     x(i) = ~isempty(hits{i});
% end
%
% GROUP1 = x';
%
% clear hits x;
%
% [hits] = regexp(SUBJECTS,GROUP2,'match');
%
% for i = 1:length(hits)
%     x(i) = ~isempty(hits{i});
% end
%
% GROUP2 = x' * 2;
%
% clear hits x;
%
% GROUPS = GROUP1 + GROUP2

GROUPS = {...
'1',
'1',
'1',
'1',
'1',
'1',
'1',
'1',
'1',
'1',
'1',
'1',
'1',
'1',
'1',
'1',
'1',
'1',
'1',
'1',
'1',
'1',
'1',
'1',
'2',
'2',
'2',
'2',
'2',
'2',
'2',
'2',
'2',
'2',
'2',
'2',
'2',
'2',
'2',
'2',
'2',
'2',
'2',
'3',
'3',
'3',
'3',
'3',
'3',
'3',
'3',
'3',
'3',
'3',
'3',
'3',
'3',
'3',
'3',
'3',
'3',
'3',
'3',
'3',
'3',
'3',
'3',
'3',
'3',
'3',
'3',
'3',
'3',
'3'};

SUBJECTS = {...
'31700',
'31920',
'32362',
'32436',
'32545',
'32676',
'32677',
'32682',
'32702',
'32762',
'32763',
'33210',
'33237',
'33462',
'33659',
'33699',
'33748',
'33781',
'33792',
'33869',
'33995',
'34040',
'35125',
'35850',
'31835',
'32060',
'32208',
'32443',
'32468',
'32574',
'32768',
'33475',
'34229',
'35078',
'35179',
'35322',
'35380',
'35652',
'35751',
'36057',
'36080',
'36324',
'36463',
'31857',
'31931',
'31933',
'31953',
'32105',
'32111',
'32120',
'32226',
'32235',
'32242',
'32378',
'32552',
'32568',
'32616',
'32697',
'32723',
'32839',
'32852',
'33222',
'33249',
'33505',
'33543',
'33624',
'33676',
'33897',
'33921',
'34032',
'34127',
'35077',
'35948',
'36349'};

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Read data from FeatQuery's output (ie, 'report.txt' files)

data = struct('group',[],'subject',[],'region',[],'signal',[],'signalmedian',[]);

for s = 1:length(SUBJECTS)

    % Specify current Subject ID
    SUBJ = SUBJECTS{s};
    GRP  = GROUPS(s);

    for r = 1:length(REGIONS)

        % Specify current Region
        ROI = REGIONS{r};

        % Buffer for group
        G(r,1) = GROUPS(s);

        % Buffer for subject number
        S(r,1) = str2num(SUBJ);

        % Buffer for this subject's set of regions
        R(r,1) = cellstr(ROI);


        for c = 1:length(COPES)

            % Specify current COPE
            COPE = ['cope',num2str(COPES(c))];

            % Specify data file to read
            FILE = fullfile(IPATH,SUBJ,COPE,ROI,'report.txt');

            % Check to make sure the data file exists
            if exist(FILE)~=2
                disp(SUBJ)
                disp(ROI)
                disp('FQ report is missing')
            end

            FID = fopen(FILE,'r');
            % Read and ignore first 5 values
            fscanf(FID,'%s',5);
            % Read and store Parameter Estimate data in buffer
            P(r,c) = fscanf(FID,'%f',1);
            Q(r,c) = fscanf(FID,'%f',1);
            fclose(FID);

        end % copes


    end % regions

    % Put data together in one struct
    data.group   = [data.group; G];
    data.subject = [data.subject; S];
    data.region  = [data.region; R];
    data.signal  = [data.signal; P];
    data.signalmedian  = [data.signal; Q];

    clear G S R P Q;

end % subjects

save data

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Descriptive statistics for each COPE across ROIs and groups

groupidx1 = find(ismember(data.group, '1'));
groupidx2 = find(ismember(data.group, '2'));
groupidx3 = find(ismember(data.group, '3'));
signal1 = data.signal(groupidx1,:);
signal2 = data.signal(groupidx2,:);
signal3 = data.signal(groupidx3,:);
% Look of plot
L1 = 'b.'
L2 = 'r.'
L3 = 'k.'

figure(1)
% No Risk
Y1 = signal1(:,1);
Y2 = signal2(:,1);
Y3 = signal3(:,1);
P1 = 0.8;
P2 = 1.0;
P3 = 1.2;
plot(P1,Y1,L1,P2,Y2,L2,P3,Y3,L3)
hold on
boxplot(Y1,'position',P1,'colors','k')
hold on
boxplot(Y2,'position',P2,'colors','k')
hold on
boxplot(Y3,'position',P3,'colors','k')
hold on
% Reward Risk
Y1 = signal1(:,2);
Y2 = signal2(:,2);
Y3 = signal3(:,2);
P1 = 1.8;
P2 = 2.0;
P3 = 2.2;
plot(P1,Y1,L1,P2,Y2,L2,P3,Y3,L3)
hold on
boxplot(Y1,'position',P1,'colors','k')
hold on
boxplot(Y2,'position',P2,'colors','k')
hold on
boxplot(Y3,'position',P3,'colors','k')
hold on
% Behavioral Risk
Y1 = signal1(:,3);
Y2 = signal2(:,3);
Y3 = signal3(:,3);
P1 = 2.8;
P2 = 3.0;
P3 = 3.2;
plot(P1,Y1,L1,P2,Y2,L2,P3,Y3,L3)
hold on
boxplot(Y1,'position',P1,'colors','k')
hold on
boxplot(Y2,'position',P2,'colors','k')
hold on
boxplot(Y3,'position',P3,'colors','k')
ylabel('Mean % Signal Change')
title('Hi-Risk, CUD, & Control within each condition')
set(gca,...
    'YLim',[-0.2 0.4], ...
    'XLim',[0.5 3.5], ...
    'XTick',[1 2 3],...
    'XTickLabel',{'No Risk', 'Reward Risk', 'Behavioral Risk'})




% Plot along
%groupidx1 = find(ismember(data.group, '1'));
%groupidx2 = find(ismember(data.group, '2'));
%groupidx3 = find(ismember(data.group, '3'));
%signal1 = data.signal(groupidx1,:);
%signal2 = data.signal(groupidx2,:);
%signal3 = data.signal(groupidx3,:);

figure(2)
% Hi-risk
Y1 = signal1(:,1);
Y2 = signal1(:,2);
Y3 = signal1(:,3);
P1 = 0.8;
P2 = 1.0;
P3 = 1.2;
plot(P1,Y1,L1,P2,Y2,L1,P3,Y3,L1)
hold on
boxplot(Y1,'position',P1,'colors','k')
hold on
boxplot(Y2,'position',P2,'colors','k')
hold on
boxplot(Y3,'position',P3,'colors','k')
hold on
% CUD
Y1 = signal2(:,1);
Y2 = signal2(:,2);
Y3 = signal2(:,3);
P1 = 1.8;
P2 = 2.0;
P3 = 2.2;
plot(P1,Y1,L2,P2,Y2,L2,P3,Y3,L2)
hold on
boxplot(Y1,'position',P1,'colors','k')
hold on
boxplot(Y2,'position',P2,'colors','k')
hold on
boxplot(Y3,'position',P3,'colors','k')
hold on
% Controls
Y1 = signal3(:,1);
Y2 = signal3(:,2);
Y3 = signal3(:,3);
P1 = 2.8;
P2 = 3.0;
P3 = 3.2;
plot(P1,Y1,L3,P2,Y2,L3,P3,Y3,L3)
hold on
boxplot(Y1,'position',P1,'colors','k')
hold on
boxplot(Y2,'position',P2,'colors','k')
hold on
boxplot(Y3,'position',P3,'colors','k')
ylabel('Mean % Signal Change')
title('NR, RR, & BR within each subject group')
set(gca,...
    'YLim',[-0.2 0.4], ...
    'XLim',[0.5 3.5], ...
    'XTick',[1 2 3],...
    'XTickLabel',{'Hi-Risk', 'CUD', 'Controls'})





%%%%%%%%
Y  = data.signal;
g1 = data.region;
g2 = data.group;
GROUP = {g1 g2};
% 'mean'     mean
% 'sem'      standard error of the mean
% 'numel'    count, or number of elements
% 'gname'    group name
% 'std'      standard deviation
% 'var'      variance
% 'min'      minimum
% 'max'      maximum
% 'range'    maximum - minimum
% 'meanci'   95% confidence interval for the mean
% 'predci'   95% prediction interval for a new observation
WHICHSTATS = {'gname' 'mean' 'sem' 'numel' 'min' 'max' 'range'};
[grp,avg,se,num,lo,hi,range] = grpstats(Y, GROUP, WHICHSTATS)

% Examples:
%       load carsmall
%       [m,p,g] = grpstats(Weight,Model_Year,{'mean','predci','gname'})
%       n = length(m)
%       errorbar((1:n)',m,p(:,2)-m)
%       set(gca,'xtick',1:n,'xticklabel',g)
%       title('95% prediction intervals for mean weight by year')

% check stats


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Display data

%figure
%bar(avg)
%ylabel('% Signal Change')
%xlabel('Hirisk                         CUD                          Control')

%for i = 1:length(g)
%
%    figure(i)
%    %bar(m(i:i+1,:))
%    bar(m(i,:))
%    ylabel('% Signal Change')
%    xlabel('COPES')
%    hold on
%    errorbar(m(i,:),s(i,:))
%
%
%
%end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%   % Statistics
%
%   % Two-way ANOVA = 2 (Groups) X 3 (Conditions) X 4 (Regions)
%
%   % Reorganize data so that response data is in one vector
%   response = vertcat(data.signal(:,1),data.signal(:,2),data.signal(:,3));
%
%   p1 = vertcat(g2,g2,g2); % groups
%
%   c1 = ones(length(data.signal),1);
%   c2 = ones(length(data.signal),1) * 2;
%   c3 = ones(length(data.signal),1) * 3;
%   p2 = vertcat(c1,c2,c3); % conditions
%
%   p3 = vertcat(g1,g1,g1); % regions
%
%   predictors = {p1 p2 p3};
%   predictor_names = strvcat('Group','Condition','Region');
%
%   [pvalue,table,sem] = anovan(response, predictors, ...
%                             'model','full', 'display','off', ...
%                             'varnames',predictor_names )
%

%end %  function