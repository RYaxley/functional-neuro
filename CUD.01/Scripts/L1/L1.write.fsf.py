#!/usr/bin/env python

import sys
import os
import re
import string
import numpy as np


model = sys.argv[1]

if model == 'Decision.100423':
    evs = ['NR', 'RR', 'BR', 'Resp', 'NoResp']
elif model == 'Outcome.100708':
    evs = ['NR_R', 'RR_R', 'RR_U', 'BR_R', 'BR_U', 'Stim']

fsf = model+'.fsf'
task = model.split('.')[0]
version = model.split('.')[1]


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
    
data = os.path.join(exp_remote, 'Analysis', 'Images')
scripts = os.path.join(exp_local, 'Scripts')
template = os.path.join(scripts, 'L1', fsf)
opath = os.path.join(exp_local, 'Analysis', task, version, 'L1')
try:
    os.mkdir(opath)
except OSError:
    pass

# Load subjects
fid = os.path.join(exp_remote, 'Scripts', 'Subjects', 'subjects.py')
f = file(fid)
exec(f)
f.close()
subjects = dict(subjects)

# Load FSL template
f = file(fsf)
design = f.read()
f.close()


for subj, info in sorted(subjects.iteritems()):  
    
    if info[10] == 'Y':

        for sess in range(1, 7):

            # If this run is usable, go ahead
            if info[sess]:
                if info[0] <= 3:
                    volumes = 180 # Specify number of volumes for this subject
                    TR = '2.0'
                    anat1 = os.path.join(data, subj, '300_brain')
                    if subj == '31700':
                        disdaqs = 0 # Volumes removed from start of scan 
                    else:
                        disdaqs = 4                      
                    ipath = os.path.join(exp_remote, 'Analysis', 'PS', str(disdaqs)+'disdaqs')
                elif info[0] >= 4:
                    volumes = 410
                    TR = '1.5'
                    anat1 = os.path.join(data, subj, '002_brain')
                    disdaqs = 0
                    ipath = os.path.join(exp_remote, 'Analysis', 'PS', str(disdaqs)+'disdaqs')
                volumes = str(volumes - disdaqs)

                output = os.path.join(opath, subj, str(sess).zfill(2))

                func = os.path.join(ipath, subj, str(sess).zfill(2)+'.feat', 'filtered_func_data')
                
                evpath = os.path.join(exp_local, 'Analysis', 'EV', subj, str(sess).zfill(2) + '.')
                ev1 = os.path.join(evpath + evs[0] + '.txt')
                ev2 = os.path.join(evpath + evs[1] + '.txt')
                ev3 = os.path.join(evpath + evs[2] + '.txt')
                ev4 = os.path.join(evpath + evs[3] + '.txt')
                ev5 = os.path.join(evpath + evs[4] + '.txt')
        
                subs = {'set fmri(outputdir) "' : 'set fmri(outputdir) "' + output,
                        'set fmri(tr) 2.0' : 'set fmri(tr) ' + TR,
                        'set highres_files(1) "' : 'set highres_files(1) "' + anat1,
                        'set feat_files(1) "' : 'set feat_files(1) "' + func,
                        'set fmri(npts) 180' : 'set fmri(npts) ' + volumes,
                        'set fmri(custom1) "' : 'set fmri(custom1) "' + ev1,
                        'set fmri(custom2) "' : 'set fmri(custom2) "' + ev2,
                        'set fmri(custom3) "' : 'set fmri(custom3) "' + ev3,
                        'set fmri(custom4) "' : 'set fmri(custom4) "' + ev4,
                        'set fmri(custom5) "' : 'set fmri(custom5) "' + ev5,
                        '/usr/local/fsl/data/standard/MNI152_T1_2mm_brain': data+'/MNI152_T1_2mm_brain',
                         }
                
                if np.size(evs) == 6:
                    ev6 = os.path.join(evpath + evs[5] + '.txt')
                    subs = { 'set fmri(custom6) "' : 'set fmri(custom6) "' + ev6 }
                
                temp = design
                for old, new in subs.iteritems():
                    temp = temp.replace(old, new)
        
                # Write to cluster home
                fid = '.'.join([model, subj, str(sess), 'fsf'])
                fid = os.path.join(exp_local, 'Scripts', 'L1', 'FSF', fid)
                x = file(fid, 'w')
                x.write(temp)
                x.close()
                # Write to munin
                fid = '.'.join([model, subj, str(sess), 'fsf'])
                fid = os.path.join(exp_remote, 'Scripts', 'L1', 'FSF', fid)
                x = file(fid, 'w')
                x.write(temp)
                x.close()
                