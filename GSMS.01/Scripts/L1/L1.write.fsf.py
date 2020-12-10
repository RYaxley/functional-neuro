#!/usr/bin/env python

import sys
import os
import re
import string
import scipy as S

#---------------------------------------------------------------------------#
ev = ['', '', '', '']


# model = 'LA.110413'
# ev[0] = 'Gain'
# ev[1] = 'Loss'
# ev[2] = 'Miss'

# model = 'LA.100309'
# ev[0] = 'Stim'

# model = 'LA.100311'
# ev[0] = 'Stim'
# ev[1] = 'Resp'

# model = 'LA.100315'
# ev[0] = 'Stim'
# ev[1] = 'Resp'
# ev[2] = 'Miss'

# model = 'LA.100317'
# ev[0] = 'Stim'
# ev[1] = 'Resp'
# ev[2] = 'Gain'
# ev[3] = 'Loss'

# model = 'LA.110214'
# ev[0] = 'Stim'
# ev[1] = 'Gain'
# ev[2] = 'Loss'

model = 'LA.110503'
ev[0] = 'Stim'
ev[1] = 'Gain'
ev[2] = 'Loss'

# * * *

# model = 'TD.100309'
# ev[0] = 'Stim'

# model = 'TD.100311'
# ev[0] = 'Stim'
# ev[1] = 'Resp'

# model = 'TD.100315'
# ev[0] = 'Stim'
# ev[1] = 'Resp'
# ev[2] = 'Miss'

# model = 'TD.100317'
# ev[0] = 'Stim'
# ev[1] = 'Resp'
# ev[2] = 'Stim.SSR.Scaled'
# ev[3] = 'Stim.LLR.Scaled'

# model = 'TD.100319'
# evs = ['Stim', 'Resp', 'Gain', 'Loss']

# model = 'TD.100323'
# evs = ['Stim', 'Resp', 'Gain', 'Loss']

# model = 'TD.110211'
# ev[0] = 'Stim'
# ev[1] = 'LLR'

# model = 'TD.110214'
# ev[0] = 'Stim'
# ev[1] = 'SSR'
# ev[2] = 'LLR'
#---------------------------------------------------------------------------#

fsf = model+'.fsf'
task = model.split('.')[0]
version = model.split('.')[1]

# Specify paths
study = 'GSMS.01'

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

disdaqs = 5 # Volumes removed from start of scan                      
ipath = os.path.join(exp_remote, 'Analysis', 'PS', str(disdaqs)+'disdaqs')
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

# Real Session # from scanner
if task == 'LA':
    firstrun = 1
    lastrun = 5
elif task == 'TD':
    firstrun = 5
    lastrun = 9
elif task == 'Outcome':
    firstrun = 9
    lastrun = 9

for subj, info in sorted(subjects.iteritems()):

    for sess in range(firstrun, lastrun):

        # If this subject and session are used, proceed
        if (info[3] == 'Y') and (info[sess + 3] != 0):

            # Specify number of volumes for this run
            if sess < 9:
                volumes = info[1]
            elif sess == 9:
                volumes = info[2]
            volumes = str(volumes - disdaqs)

            # Anatomicals
            if os.path.isfile(os.path.join(data, subj, '300_brain.nii.gz')):
                anat1 = os.path.join(data, subj, '300_brain')
            elif os.path.isfile(os.path.join(data, subj, '003_brain.nii.gz')):
                anat1 = os.path.join(data, subj, '003_brain')
            # Secondary Anatomical
            if os.path.isfile(os.path.join(data, subj, '400_brain.nii.gz')):
                anat2 = os.path.join(data, subj, '400_brain')
            elif os.path.isfile(os.path.join(data, subj, '004_brain.nii.gz')):
                anat2 = os.path.join(data, subj, '004_brain')
            
            # Functional
            func = os.path.join(ipath, subj, str(sess).zfill(2)+'.feat', 'filtered_func_data')
            
            # Output and EV
            if task == 'LA':
                output = os.path.join(opath, subj, str(sess).zfill(2))
                evpath = os.path.join(exp_remote, 'Analysis', 'EV', subj, task + '.' + str(sess).zfill(2) + '.')
            elif task == 'TD':
                output = os.path.join(opath, subj, str(sess-4).zfill(2))
                evpath = os.path.join(exp_remote, 'Analysis', 'EV', subj, task + '.' + str(sess-4).zfill(2) + '.')

            ev1 = os.path.join(evpath + ev[0] + '.txt')
            ev2 = os.path.join(evpath + ev[1] + '.txt')
            ev3 = os.path.join(evpath + ev[2] + '.txt')
            ev4 = os.path.join(evpath + ev[3] + '.txt')

            subs = {'set fmri(outputdir) "' : 'set fmri(outputdir) "' + output,
                    'set highres_files(1) "' : 'set highres_files(1) "' + anat1,
                    'set feat_files(1) "' : 'set feat_files(1) "' + func,
                    'set fmri(npts) 211' : 'set fmri(npts) ' + volumes,
                    'set fmri(custom1) "' : 'set fmri(custom1) "' + ev1,
                    'set fmri(custom2) "' : 'set fmri(custom2) "' + ev2,
                    'set fmri(custom3) "' : 'set fmri(custom3) "' + ev3,
                    'set fmri(custom4) "' : 'set fmri(custom4) "' + ev4,
                    '/usr/local/fsl/data/standard/MNI152_T1_2mm_brain': data+'/MNI152_T1_2mm_brain',
                     }
                     
            temp = design
            for old, new in subs.iteritems():
                temp = temp.replace(old, new)
                
            # Write new template file to home directory
            fid = '.'.join([model, subj, str(sess), 'fsf'])
            fid = os.path.join(exp_local, 'Scripts', 'L1', 'FSF', fid)
            x = file(fid, 'w')
            x.write(temp)
            x.close()
            # Write new template file to experiment directory on Munin
            fid = '.'.join([model, subj, str(sess), 'fsf'])
            fid = os.path.join(exp_remote, 'Scripts', 'L1', 'FSF', fid)
            x = file(fid, 'w')
            x.write(temp)
            x.close()            