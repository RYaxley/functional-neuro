#!/usr/bin/env python -W ignore::DeprecationWarning
# encoding: utf-8

import sys
import os
import glob
# import xlrd
import scipy as S
import scipy.stats


model = sys.argv[1]

# Specify paths
study = 'CUD.01'

# exp_remote = CUD.01 directory on Munin
# exp_local = Scripts directory in home directory
if os.getlogin() == 'richardyaxley': # Macbook
    exp_remote = os.path.join('/Volumes', study)
    exp_local = os.path.join(os.path.expanduser('~'), study)
elif os.getlogin() == 'yaxley': # Cluster node
    exp_remote = os.path.join(os.path.expanduser('~'),'experiments', study)
    exp_local = os.path.join(os.path.expanduser('~'), study)
elif os.getlogin() == 'sb212': # Cluster node
    exp_remote = os.path.join(os.path.expanduser('~'),'net', 'munin', 'data', 'debellis', study)
    exp_local = os.path.join(os.path.expanduser('~'), study)

# Number of groups in Level 3 (1G = 1 group; 2G = 2 groups; 3G = 3 groups)
# fsf = '1G.fsf'
# fsf = '1G_cov.fsf'
# fsf = '2G_F.fsf'
fsf = '3G_F.fsf'

# Participant groupings
# grouping = 'CTRL+ADLT' # Control Paper
# grouping = 'M+F' # Males and females
grouping = 'Males' # Males only
# grouping = 'Males-AgeCutoff' # Males only

covariates = False
modelling = 2 # 1=Flame2, 2=Flame1

# Design matrix = Contrast # : EVs
if model == 'Decision.100423':
    design = {'1':  ['1',      1, 0, 0, 0, 0],
              '2':  ['1',     -1, 0, 0, 0, 0],
              '3':  ['2',      0, 1, 0, 0, 0],
              '4':  ['2',      0,-1, 0, 0, 0],
              '5':  ['3',      0, 0, 1, 0, 0],
              '6':  ['3',      0, 0,-1, 0, 0],
              '7':  ['12',     1,-1, 0, 0, 0],
              '8':  ['12',    -1, 1, 0, 0, 0],
              '9':  ['13',     1, 0,-1, 0, 0],
              '10': ['13',    -1, 0, 1, 0, 0],
              '11': ['23',     0,-1, 1, 0, 0],
              '12': ['23',     0, 1,-1, 0, 0],
              '13': ['123',   -1,-1, 2, 0, 0],
              '14': ['123',    1, 1,-2, 0, 0],
             }  
elif model == 'Outcome.100708':       
    design = {'1':  ['1',      1, 0, 0, 0, 0, 0],
              '2':  ['1',     -1, 0, 0, 0, 0, 0],
              '3':  ['2',      0, 1, 0, 0, 0, 0],
              '4':  ['2',      0,-1, 0, 0, 0, 0],
              '5':  ['3',      0, 0, 1, 0, 0, 0],
              '6':  ['3',      0, 0,-1, 0, 0, 0],
              '7':  ['4',      0, 0, 0, 1, 0, 0],
              '8':  ['4',      0, 0, 0,-1, 0, 0],
              '9':  ['5',      0, 0, 0, 0, 1, 0],
              '10': ['5',      0, 0, 0, 0,-1, 0],
              '11': ['12345',  2, 2,-3, 2,-3, 0],
              '12': ['12345', -2,-2, 3,-2, 3, 0],
              '13': ['12',    -1, 1, 0, 0, 0, 0],
              '14': ['12',     1,-1, 0, 0, 0, 0],
              '15': ['24',     0, 1, 0,-1, 0, 0],
              '16': ['24',     0,-1, 0, 1, 0, 0],
              '17': ['23',     0, 1,-1, 0, 0, 0],
              '18': ['23',     0,-1, 1, 0, 0, 0],
              '19': ['45',     0, 0, 0, 1,-1, 0],
              '20': ['45',     0, 0, 0,-1, 1, 0],
              '21': ['14',     1, 0, 0,-1, 0, 0],
              '22': ['14',    -1, 0, 0, 1, 0, 0],
              '23': ['2345',   0, 2,-2, 2,-2, 0],
              '24': ['2345',   0,-2, 2,-2, 2, 0],
              '25': ['6',      0, 0, 0, 0, 0, 1],
              '26': ['6',      0, 0, 0, 0, 0,-1],
             } 
else:
    'Need to specify design matrix'

contrasts = range(1, len(design)+1)
copes = range(1, len(design['1']))
jobcount = 0

# Specify more paths
scripts = os.path.join(exp_local, 'Scripts')
template = os.path.join(scripts, 'L3', fsf)
task = model.split('.')[0]
version = model.split('.')[1]
L2 = os.path.join(exp_remote, 'Analysis', task, version, 'L2')
L3 = os.path.join(exp_local, 'Analysis', task, version, 'L3')
if not os.path.isdir(L2):
    print 'Experiment directory is not available.'
    sys.exit()
try:
    os.mkdir(L3)
except OSError:
    pass

# Load subjects
fid = os.path.join(exp_remote, 'Scripts', 'Subjects', 'subjects.py')
f = file(fid)
exec(f)
f.close()
subjects = dict(subjects)


# Generate list of subjects whose data is actually available for analysis
ctrlcount = hrcount = cudcount = 0
usedsubjects = []                                                        
for subject, info in sorted(subjects.iteritems()):
    
    if info[10] == 'Y':
        
        print subject, info
        
        fid = os.path.join(L2, subject, '01.gfeat', 'cope1.feat', 'stats', 'cope1.nii.gz' )
        
        if grouping == 'CTRL+ADLT': # Participants in Control + Adults Paper - Thursday February 24, 2011
            # Adolescent Controls
            if info[0] == 1:
               if os.path.isfile(fid):
                    usedsubjects.append((subject, info))   
                    ctrlcount += 1   
            # Adult E1 and E2 participants from Huettel (2006)
            elif info[0] == 4 or info[0] == 5:
                if os.path.isfile(fid):
                    info[0] = 2 # change group number to make 2group analysis work
                    usedsubjects.append((subject, info)) 
    
        elif grouping == 'Males' or grouping == 'Males-AgeCutoff': # Three adolescent groups of Males only (November 8, 2010) 
            if info[7] == 'M':
                # Adolescent Controls
                if info[0] == 1:
                   if os.path.isfile(fid):
                        usedsubjects.append((subject, info))   
                        ctrlcount += 1   
                # Adolescent Psychiatric Controls
                elif info[0] == 2:
                    if os.path.isfile(fid):
                        usedsubjects.append((subject, info))
                        hrcount += 1 
                # Adolescent CUD
                elif info[0] == 3:
                    if os.path.isfile(fid):
                        usedsubjects.append((subject, info)) 
                        cudcount += 1  

        elif grouping == 'M+F': # Two adolescent groups (May 3, 2011) 
            # Adolescent Controls
            if info[0] == 1:
               if os.path.isfile(fid):
                    usedsubjects.append((subject, info))   
                    ctrlcount += 1   
            # Adolescent Psychiatric Controls
            elif info[0] == 2:
                if os.path.isfile(fid):
                    usedsubjects.append((subject, info))
                    hrcount += 1 
        
        else:
            print 'Need to specify subject grouping'

usedsubjects = dict(usedsubjects)
print 'CTRL=', ctrlcount, 'HR=', hrcount, 'CUD=', cudcount, 'Total=', ctrlcount+hrcount+cudcount

# print 'Removing 33792 from analysis'
# del usedsubjects['33792'] 

# Extract ages for CUD group (February 2, 2011)
if grouping.endswith('AgeCutoff'):
    ages = []
    for subject, info in sorted(usedsubjects.iteritems()):
        if info[0] == 3: # CUD group
            ages.append(float(info[8]))
    print ages
    ageCutoff = min(ages) - 0.5 # 6 months
    print 'Age Cutoff:', ageCutoff

    # Exclude subjects that are less than Age Cutoff
    for subject, info in sorted(usedsubjects.iteritems()):
        if float(info[8]) < ageCutoff:
            print subject, info[0], info[8], float(info[8]) < ageCutoff
            del(usedsubjects[subject])

usedsubjects

# Recount number of subjects in groups
ctrlcount = hrcount = cudcount = 0
for subject, info in sorted(usedsubjects.iteritems()):
    # Adolescent Controls
    if info[0] == 1: ctrlcount += 1   
    # Adolescent Psychiatric Controls
    elif info[0] == 2: hrcount += 1 
    # Adolescent CUD
    elif info[0] == 3: cudcount += 1
print 'Recount: CTRL=', ctrlcount, 'HR=', hrcount, 'CUD=', cudcount, 'Total=', ctrlcount+hrcount+cudcount


############################################################################      
'''
# Covariates
if covariates:
    print 'Including Covariates'
    if fsf.find('cov'):
        # Load subjects' neuropsych data
        fid = os.path.join(exp_local, 'Data', 'Neuropsych', 'CANNABIS_05062010.xls')
        workbook = xlrd.open_workbook(fid)
        sheet = workbook.sheet_by_index(0)
    
        for col in range(sheet.ncols):
            var = str(sheet.cell_value(rowx=0,colx=col)).strip('#')
            exec var + '= sheet.col_values(col)[1:]'
      
        # Reduce BIAC ID #
        for i in range(len(BIAC)): 
            BIAC[i] = str(BIAC[i]).split('.')[0]
    
        Convert covariate to integer

        Executive Control - Tower Sub Achievement
        covariate = TOWER_SUB_ACHIEVE
        covname = 'TOWER'

        Wisconsin Card Sort Categories Completed-Standard Score
        covariate = WCST_CAT_COMP_SS
        covname = 'WCST'

        Attention - Errors of Omission - T-score
        covariate = CCPT_EO_T
        covname = 'EO'

        Impulsivity - Errors of Commission - T-score
        covariate = CCPT_EC_T
        covname = 'EC'
    
        June 18, 2010 - More variables recommended by Steve Hooper

        Wisconsin Perseveration Score - Flexiblity
        covariate = WCST_PERS_RESP_STAN
        covname = 'WCST_PERS'    
    
        Tower Sub Mean Scaled - Planning & Problem Solving
        covariate = TOWER_SUB_MEAN_SCALED
        covname = 'TOWER_MEAN' 
    
        Verbal Fluency - Verbal Efficiency
        covariate = VER_FLU_SUB_CATEGORY
        covname = 'VERBAL_FLUENCY'     
    
        WJIII AWM Cluster - Verbal Working Memory 
        covariate = WJIII_AUD_MEM_CLUSTER_SS
        covname = 'WJ_AWM'     
            
        for i in range(len(covariate)):
            try: 
                covariate[i] = float(covariate[i])
            except:
                covariate[i] =  S.nan
            
        # Demean
        covariate = covariate - S.stats.nanmean(covariate)    
            
        cov = dict(zip(BIAC, covariate))    
            
        # Append the covariate values to the subject-info dictionary
        for subj, value in sorted(cov.iteritems()):
            if usedsubjects.has_key(subj):
                if S.isnan(value):
                    print subj, value
                    del(usedsubjects[subj])
                else:
                    usedsubjects[subj] += [value]
            else:
                print subj, 'Covariate Missing'
else:
    'No covariates'
    pass
'''
#############################################################################
for contrast in sorted(design.iterkeys()):
    
    # Check to see if data exists for this subject & this contrast.
    volumes = []
    for subject, info in sorted(usedsubjects.iteritems()):
        
        fid = os.path.join(L2, subject, contrast.zfill(2)+'.gfeat')
        if os.path.isdir(fid):
             # Check for only 1 input into L2
             try:
                 f = open(os.path.join(fid, 'design.mat') )
                 x = f.readlines()
                 f.close()
                 numpoints = x[1].split()[1]
                 if not numpoints == '1':
                     volumes.append((subject, info))
             except:
                 print 'Design matrix error', fid
        else:
            print 'missing', fid
    volumes = dict(volumes)
    
    # Read .fsf template
    fid = open(fsf)
    template = fid.read()
    fid.close()

    output = os.path.join(L3, fsf.split('.')[0]+'_'+grouping+'_'+str(contrast.zfill(2)))
    
    # Make gross substitions in template
    subs = {'set fmri(outputdir) "' : 'set fmri(outputdir) "'+output,
            'set fmri(npts) 99' : 'set fmri(npts) '+str(len(volumes)),
            'set fmri(multiple) 99' : 'set fmri(multiple) '+str(len(volumes)),
            'set fmri(mixed_yn) 2' : 'set fmri(mixed_yn) '+str(modelling),
           }
    for old, new in subs.iteritems():
        template = template.replace(old, new)
    
    # Make subject specific substitutions in template
    count = 0
    for subject, info in sorted(volumes.iteritems()):
        count += 1
        # Input path
        old = 'set feat_files(' +str(count)+ ') ""'
        new = 'set feat_files(' +str(count)+ ') "' +os.path.join(L2, subject, contrast.zfill(2)+'.gfeat', 'cope1.feat')+'"'
        template = template.replace(old, new)
        
        # Group membership
        old = 'set fmri(groupmem.' +str(count)+ ') 0'
        new = 'set fmri(groupmem.' +str(count)+ ') '+str(info[0])
        template = template.replace(old, new)
        
        # Covariate value
        if fsf == '1group_cov.fsf':
            old = 'set fmri(evg' +str(count)+ '.2) 0'
            new = 'set fmri(evg' +str(count)+ '.2) ' + str(info[11])
            template = template.replace(old, new)

        # EV value based on group
        for i in range(1,4):
            if info[0]==i:
                old = 'set fmri(evg' +str(count)+ '.'+str(i)+') 0'
                new = 'set fmri(evg' +str(count)+ '.'+str(i)+') 1'
                template = template.replace(old, new)
                
    # Write new .fsf template
    fid = os.path.join(exp_local, 'Scripts', 'L3', 'FSF', model+'.'+fsf.split('.')[0]+'_'+grouping+'.'+str(contrast.zfill(2)))
    fid = '.'.join([fid, 'fsf'])
    f = file(fid, 'w')
    f.write(template)
    f.close()
    # Write new .fsf template
    fid = os.path.join(exp_remote, 'Scripts', 'L3', 'FSF', model+'.'+fsf.split('.')[0]+'_'+grouping+'.'+str(contrast.zfill(2)))
    fid = '.'.join([fid, 'fsf'])
    f = file(fid, 'w')
    f.write(template)
    f.close()
