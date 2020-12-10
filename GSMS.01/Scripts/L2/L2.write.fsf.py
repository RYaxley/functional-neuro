#!/usr/bin/env python

import sys
import os
import re
import string
              
#############################################################################
# Design matrix = Contrast # : EVs

# model = 'LA.110413' 
# design = {'1':  ['1',  1, 0],
#           '2':  ['1',  0, 1],
#           '3':  ['2',  1,-1],
#           '4':  ['2', -1, 1],
#          }
#---------------------------------------------------------------------------#
# model = 'LA.100309'
# model = 'TD.100309'
# design = {'1':  ['1',  1],
#           '2':  ['1', -1],
#          } 
#---------------------------------------------------------------------------#
# model = 'LA.100311'
# model = 'TD.100311' 
# model = 'TD.110211' 
# design = {'1':  ['1',  1, 0],
#           '2':  ['1', -1, 0],
#           '3':  ['2',  0, 1],
#           '4':  ['2',  0,-1],
#          }
#---------------------------------------------------------------------------#
# model = 'LA.100315'
# model = 'TD.100315' 
# model = 'LA.110214'
# # model = 'TD.110214'
model = 'LA.110503'
design = {'1':  ['1',  1, 0, 0],
          '2':  ['1', -1, 0, 0],
          '3':  ['2',  0, 1, 0],
          '4':  ['2',  0,-1, 0],
          '5':  ['3',  0, 0, 1],
          '6':  ['3',  0, 0,-1],
         }
#---------------------------------------------------------------------------#
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
fsf = 'L2.fsf' 
task = model.split('.')[0]
version = model.split('.')[1]

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

# data = os.path.join(exp_remote, 'Analysis', 'Images')
scripts = os.path.join(exp_local, 'Scripts') 
L1 = os.path.join(exp_remote, 'Analysis', task, version, 'L1')
L2 = os.path.join(exp_remote, 'Analysis', task, version, 'L2')    
try:
    os.mkdir(L2)
except OSError:
    pass
    
try:
    os.mkdir(os.path.join(scripts, 'L2', 'FSF'))
except OSError:
    pass

                         
contrasts = range(1, len(design)+1)
copes = range(1, len(design['1']))
          
# Load subjects
fid = os.path.join(exp_remote, 'Scripts', 'Subjects', 'subjects.py')
f = file(fid)
exec(f)
f.close()
subjects = dict(subjects)   


if task == 'LA':
    firstrun = 1
    lastrun = 5
elif task == 'TD':
    firstrun = 1
    lastrun = 5
elif task == 'Outcome':
    firstrun = 9
    lastrun = 9

for subject, info in sorted(subjects.iteritems()):         
    if info[3] == 'Y':  
        for contrast, cope in sorted(design.iteritems()): 
              
            subjectpath = os.path.join(L1, subject)
            copelist = []           
            
            for used in info[firstrun+3: lastrun+3 ]: 
                if used:   

                    featdir = os.path.join(subjectpath, str(used).zfill(2)+'.feat') 
                    empty = False

                    for i in cope[0]:       
                        fid = os.path.join(featdir, 'tsplot', 'ps_tsplot_zstat1_ev'+str(i)+'.txt')
                        if not os.path.exists(fid):  
                            empty = True              
                    if not empty:
                        copelist.append(os.path.join(featdir, 'stats', 'cope'+contrast))   
            
            if len(copelist) > 1:    
            
                # Read .fsf template
                fid = open(fsf)
                template = fid.read()
                fid.close()  
            
                # Substitutions
                output = os.path.join(L2, subject.split('/')[-1], contrast.zfill(2))
                volumes = str(len(copelist))
                
                subs = {'set fmri(outputdir) "' : 'set fmri(outputdir) "' + output,
                        'set fmri(npts) 6' : 'set fmri(npts) ' + volumes,
                        'set fmri(multiple) 6' : 'set fmri(multiple) ' + volumes,
                       }
                for old, new in subs.iteritems():
                    template = template.replace(old, new)
                
                for i in range(len(copelist)):
                    old = 'set feat_files('+str(i+1)+') ""'
                    new = 'set feat_files('+str(i+1)+') "'+copelist[i]+'"'
                    template = template.replace(old, new)
                
                # Write new .fsf template
                fid = os.path.join(exp_local, 'Scripts', 'L2', 'FSF', model+'.'+subject.split('/')[-1]+'.'+str(contrast.zfill(2)))
                fid = '.'.join([fid, 'fsf'])
                f = file(fid, 'w')
                f.write(template)
                f.close()
                fid = os.path.join(exp_remote, 'Scripts', 'L2', 'FSF', model+'.'+subject.split('/')[-1]+'.'+str(contrast.zfill(2)))
                fid = '.'.join([fid, 'fsf'])
                f = file(fid, 'w')
                f.write(template)
                f.close()