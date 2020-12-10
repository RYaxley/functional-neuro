function roi_plot(EXP,MODEL,REGIONS)
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
SUBYEAR='200'
SUBJECTS = find_subjects(IPATH,SUBYEAR);

% Set the EV numbers corresponding to C, RR, and BR COPES
COPES = [1,3,5];

% Set the regions-of-interest to process (excluding filename suffix)
REGIONS = { 'pcc' };

% Set a vector to identify the two groups (eg, Adults = 1, Kids = 2)
GROUP1 = '200[35]';
GROUP2 = '200[678]';

[hits] = regexp(SUBJECTS,GROUP1,'match');

for i = 1:length(hits)
    x(i) = ~isempty(hits{i});
end

GROUP1 = x';

clear hits x;

[hits] = regexp(SUBJECTS,GROUP2,'match');

for i = 1:length(hits)
    x(i) = ~isempty(hits{i});
end

GROUP2 = x' * 2;

clear hits x;

GROUPS = GROUP1 + GROUP2;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Read data from FeatQuery's output (ie, 'report.txt' files)

data = struct('group',[],'subject',[],'region',[],'signal',[]);

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
        S(r,1) = str2num(SUBJ(10:end));

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
            fclose(FID);

        end % copes


    end % regions

    % Put data together in one struct
    data.group   = [data.group; G];
    data.subject = [data.subject; S];
    data.region  = [data.region; R];
    data.signal  = [data.signal; P];

    clear G S R P;


end % subjects

save data

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Descriptive statistics for each COPE across ROIs and groups

y  = data.signal;
g1 = data.region;
g2 = data.group;
group = {g1 g2};
stats = {'gname' 'mean' 'sem'};
[g,m,s] = grpstats(y, group, stats)

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Display data

figure
bar(m)
ylabel('% Signal Change')
xlabel('COPES')

for i = 1:2:length(g)

    figure(i)
    bar(m(i:i+1,:))
    ylabel('% Signal Change')
    xlabel('COPES')
    hold on
    errorbar(m(i:i+1,:),s(i:i+1,:))

end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Statistics

% Two-way ANOVA = 2 (Groups) X 3 (Conditions) X 4 (Regions)

% Reorganize data so that response data is in one vector
response = vertcat(data.signal(:,1),data.signal(:,2),data.signal(:,3));

p1 = vertcat(g2,g2,g2); % groups

c1 = ones(length(data.signal),1);
c2 = ones(length(data.signal),1) * 2;
c3 = ones(length(data.signal),1) * 3;
p2 = vertcat(c1,c2,c3); % conditions

p3 = vertcat(g1,g1,g1); % regions

predictors = {p1 p2 p3};
predictor_names = strvcat('Group','Condition','Region');

[pvalue,table,sem] = anovan(response, predictors, ...
                          'model','full', 'display','off', ...
                          'varnames',predictor_names )


end %  function