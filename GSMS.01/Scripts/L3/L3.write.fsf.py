#!/usr/bin/env python
# encoding: utf-8
"""
L3.write.fsf.py

Created by Richard Yaxley on 2009-12-04.
"""

import sys
import os
import re
import string
import glob
import numpy as np


# Design matrix = Contrast # : EVs

# model = 'LA.110413' 
# design = {'1':  ['1',  1, 0],
#           '2':  ['1',  0, 1],
#           '3':  ['2',  1,-1],
#           '4':  ['2', -1, 1],
#          }
         
         
# model = 'LA.100309'
# model = 'TD.100309'
# design = {'1':  ['1',  1],
#           '2':  ['1', -1],
#          } 

# model = 'LA.100311'
# model = 'TD.100311' 
# model = 'TD.110211' 
# design = {'1':  ['1',  1, 0],
#           '2':  ['1', -1, 0],
#           '3':  ['2',  0, 1],
#           '4':  ['2',  0,-1],
#          }

# model = 'LA.100315'
# model = 'TD.100315' 
# model = 'LA.110214'
# model = 'TD.110214'
model = 'LA.110503'
design = {'1':  ['1',  1, 0, 0],
          '2':  ['1', -1, 0, 0],
          '3':  ['2',  0, 1, 0],
          '4':  ['2',  0,-1, 0],
          '5':  ['3',  0, 0, 1],
          '6':  ['3',  0, 0,-1],
         }

# model = 'LA.100317' 
# model = 'TD.100317'      
# design = {'1':  ['1',      1, 0, 0, 0],
#           '2':  ['1',     -1, 0, 0, 0],
#           '3':  ['2',      0, 1, 0, 0],
#           '4':  ['2',      0,-1, 0, 0],
#           '5':  ['3',      0, 0, 1, 0],
#           '6':  ['3',      0, 0,-1, 0],
#           '7':  ['4',      0, 0, 0, 1],
#           '8':  ['4',      0, 0, 0,-1],
#          }
 
#---------------------------------------------------------------------------#       
study = 'GSMS.01'
fsf = '1G.fsf'
modelling = 2        
task = model.split('.')[0]
version = model.split('.')[1] 
         
contrasts = range(1, len(design)+1)
copes = range(1, len(design['1']))

# exp_remote = GSMS.01 directory on Munin
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
    
scripts = os.path.join(exp_local, 'Scripts')
template = os.path.join(scripts, 'L3', fsf)

L2 = os.path.join(exp_remote, 'Analysis', task, version, 'L2')
L3 = os.path.join(exp_remote, 'Analysis', task, version, 'L3')
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
usedsubjects = []                                                        
for subject, info in sorted(subjects.iteritems()):
    if info[3] == 'Y':
        fid = os.path.join(L2, subject, '01.gfeat', 'cope1.feat', 'stats', 'cope1.nii.gz' )
        if os.path.isfile(fid):
            usedsubjects.append((subject, info))
usedsubjects = dict(usedsubjects)


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
                 print 'design matrix error', fid
    volumes = dict(volumes)

    # Read .fsf template
    fid = open(fsf)
    template = fid.read()
    fid.close()

    # Substitutions
    output = os.path.join(L3, fsf.split('.')[0], str(contrast.zfill(2)))

    subs = {'set fmri(outputdir) "' : 'set fmri(outputdir) "'+output,
            'set fmri(npts) 99' : 'set fmri(npts) '+str(len(volumes)),
            'set fmri(multiple) 99' : 'set fmri(multiple) '+str(len(volumes)),
            'set fmri(mixed_yn) 2' : 'set fmri(mixed_yn) '+str(modelling),
           }
    for old, new in subs.iteritems():
        template = template.replace(old, new)

    count = 0
    for subject, info in sorted(volumes.iteritems()):
        count += 1
        old = 'set feat_files(' +str(count)+ ') ""'
        new = 'set feat_files(' +str(count)+ ') "' + os.path.join(L2, subject, contrast.zfill(2)+'.gfeat', 'cope1.feat')+'"'
        template = template.replace(old, new)

        old = 'set fmri(groupmem.' +str(count)+ ') 0'
        new = 'set fmri(groupmem.' +str(count)+ ') '+str(info[0])
        template = template.replace(old, new)
        for i in range(1,4):
            if info[0]==i:
                old = 'set fmri(evg' +str(count)+ '.'+str(i)+') 0'
                new = 'set fmri(evg' +str(count)+ '.'+str(i)+') 1'
                template = template.replace(old, new)

    # Write .fsf template to home directory on Hugin
    fid = os.path.join(exp_local, 'Scripts', 'L3', 'FSF', model+'.'+fsf.split('.')[0]+'.'+str(contrast.zfill(2)))
    fid = '.'.join([fid, 'fsf'])
    f = file(fid, 'w')
    f.write(template)
    f.close()
    # Write .fsf template to experiment directory on Munin
    fid = os.path.join(exp_remote, 'Scripts', 'L3', 'FSF', model+'.'+fsf.split('.')[0]+'.'+str(contrast.zfill(2)))
    fid = '.'.join([fid, 'fsf'])
    f = file(fid, 'w')
    f.write(template)
    f.close()
