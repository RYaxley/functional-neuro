#!/usr/bin/env python
# encoding: utf-8
"""
FQ.py

Created by Richard Yaxley on 2010-02-05.

"""

import sys
import os         
import glob
import subprocess

study = 'CUD.01'
model = 'Decision.100423'          
# model = 'Outcome.100708' 

# region = '8sfg'              
# region = 'Accumbens'              
region = 'vstriatum'              

contrasts = ['02','03','04','05'] 

task = model.split('.')[0]
version = model.split('.')[1]

exp_remote = os.path.join('/Volumes', study)
exp_local = os.path.join(os.path.expanduser('~'), study)
scripts = os.path.join(os.path.join(exp_local, 'Scripts'))
L2 = os.path.join(exp_remote, 'Analysis', task, version, 'L2')
ROI =  os.path.join(exp_local, 'Analysis',task, version, 'ROI')

if not os.path.isdir(L2):
    print 'Experiment directory is not available.'
    #sys.exit()
try:
    os.mkdir(ROI)
except OSError:
    pass

# Load subject list
fid = os.path.join(scripts, 'Subjects', 'subjects.py')
f = file(fid)
exec(f)
f.close()
subjects = dict(subjects)


for contrast in contrasts:
    
    for i in glob.glob(os.path.join(L2, '?????')):   

        for cope in glob.glob(os.path.join(i, contrast+'.gfeat', 'cope1.feat' )):
    
            # Setup variables to pass to featquery
            ipath = cope       

            opath = cope.split(os.sep)     
            # opath.pop(0)
            # opath[0] = os.path.expanduser('~')
            opath[-4] = 'ROI2'   
            # opath.pop()
            # opath[-1] = opath[-1].split('.')[0]
            # opath.append(region)
            opath[-1] = region        
            opath = os.sep.join(opath)  
            try:
                os.makedirs(opath)
            except OSError:
                pass   

            opath = opath.split(os.sep)
            opath = opath[-4:]
            opath = os.sep.join(opath)
            backup = os.sep.join(['..','..','..','..',''])
            # backup = os.sep.join(['/Users','richardyaxley','CUD.01','Analysis',task,version,'Regions',''])
            opath = backup + opath

            roi = os.path.join(ROI, region)

            # Specify stats to calculate
            #STATS="6  stats/pe1
            #          stats/cope1
            #          stats/varcope1
            #          stats/tstat1
            #          stats/zstat1
            #          thresh_zstat1"
            STATS='1 stats/pe1'
        
            # FeatQuery arguments
            # -b (popup in web browser)
            # -p (convert PE to % signal change)
            # -s
            # -w (do not binarize mask)
    #        ARGS='-a 1 -p'        
            ARGS='-p -s -w'
        
            # Specify ROI mask
            # mask = '/Users/rhy/CUD.01/Analysis/Anat.ROI/HarvardOxford/Accumbens.nii.gz'
            # mask = '/Users/richardyaxley/CUD.01/Analysis/Decision/100423/Regions/ACC.nii.gz'
            mask = '/Volumes/CUD.01/Analysis/Outcome/100708/Regions/vstriatum.nii.gz'

            # Run featquery
            cmd = ['featquery 1', ipath, STATS, opath, ARGS, mask] 
            cmd = ' '.join(cmd)
            print cmd
            subprocess.Popen(cmd, shell=True).wait()                                             
        
  
        
        