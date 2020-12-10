#!/usr/bin/env python

import sys
import os
import re
import string

tr = '2'
disdaqs = '5'
smooth = '5'
cutoff = '60'

# Set paths
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
    

# latest change 
# scripts = os.path.join(exp_local, 'Scripts')
scripts = os.path.join(exp_local, 'Scripts') 


data = os.path.join(exp_remote, 'Analysis', 'Images')
analysis = os.path.join(exp_remote, 'Analysis', 'PS', disdaqs+'disdaqs') # exp_remote !!!!!!!!!!!!!!!!!!!
try:
    os.mkdir(analysis)
except OSError:
    pass

# Load Subjects
fid = os.path.join(exp_remote, 'Scripts', 'Subjects', 'subjects.py')
f = open(fid)
exec(f)
f.close()

# Load FSL template
fid = 'PS.fsf'
f = file(fid)
design = f.read()
f.close()


for s, i in sorted(subjects.iteritems()):
    
    # If usable subject
    if i[3] == 'Y':
    
        for r in range(1, 10):
            
            # If usable run
            if i[3+r] != 0:
        
                run = "%02d" %(r)
        
                if r != 9:
                    volumes = i[1]
                elif r == 9:
                    volumes = i[2]
                volumes = str(volumes)
                
                input = os.path.join(data, s)
                output = os.path.join(analysis, s, run)

                # Anatomical #1
                if os.path.isfile(os.path.join(input, '300_brain.nii.gz')):
                    anat1 = os.path.join(input, '300_brain.nii.gz')
                elif os.path.isfile(os.path.join(input, '003_brain.nii.gz')):
                    anat1 = os.path.join(input, '003_brain.nii.gz')
                
                # Anatomical #2
                if os.path.isfile(os.path.join(input, '400_brain.nii.gz')):
                    anat2 = os.path.join(input, '400_brain.nii.gz')
                elif os.path.isfile(os.path.join(input, '004_brain.nii.gz')):
                    anat2 = os.path.join(input, '004_brain.nii.gz')
        
                func = run + '.nii.gz'
                func = os.path.join(input, func)
        
                hires = os.path.join('/usr/local/packages/fsl-4.1.5/data/standard/', 'MNI152_T1_2mm_brain')
        
                subs = {'OUTPUT': output,
                        'ANATOMICAL1': anat1,
                        'ANATOMICAL2': anat2,
                        'FUNCTIONAL': func,
                        'VOLUMES': volumes,
                        'DISDAQS': disdaqs,
                        'REPTIME': tr,
                        'SMOOTH': smooth,
                        'HICUTOFF': cutoff,
                        '/usr/local/fsl/data/standard/MNI152_T1_2mm_brain': hires,
                        }
                tmp = design
                for x, y in subs.iteritems():
                    tmp = tmp.replace(x, y)

                fid = '.'.join(['PS', disdaqs+'disdaqs', s, run, 'fsf'])
                fid = os.path.join(scripts, 'PS', 'FSF', fid)
                try:
                    os.mkdir(os.path.join(scripts, 'PS', 'FSF'))
                except OSError:
                    pass
                x = file(fid, 'w')
                x.write(tmp)
                x.close()
                try:
                    os.mkdir(os.path.join(exp_remote, 'Scripts', 'PS', 'FSF'))
                except OSError:
                    pass
                x = file(fid, 'w')
                x.write(tmp)
                x.close()
