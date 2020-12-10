#!/usr/bin/env python
# encoding: utf-8
"""
scan.images.py

Copy specific Rendered Thresh z-stat images to a single local directory for quick review.

Created by Richard Yaxley on 2010-04-12.
"""

import sys
import os
import re
import shutil
import glob

# Read arguments
exp = sys.argv[1]
model = sys.argv[2]
level = sys.argv[3]

# Specify paths
analysis = os.path.join('/Volumes', exp, 'Analysis')
task = model.split('.')[0]
version = model.split('.')[1]
    
if level == 'PS':
    data = os.path.join(analysis, task, version)
else:
    data = os.path.join(analysis, task, version, level)
    
if not os.path.isdir(data):
    print 'Data Unavailable: ', data    
dstpath = os.path.join(os.path.expanduser('~'), exp, 'Analysis', task, version, level)
try: 
    os.makedirs(dstpath)
except: 
    pass


# if level == 'L2':
#     for i in glob.glob(os.path.join(data, '?????', '*.gfeat', 'cope1.feat', 'rendered_thresh_zstat1.png')): 
#         fid = i.split(os.sep)[-4]+'.'+i.split(os.sep)[-3][:2]+'.png'
#         dst = os.path.join(dstpath, fid)
#         shutil.copyfile(i,dst)
# 
# if exp == 'GSMS.01':
#     x = '*/*.gfeat'
# elif exp == 'CUD.01':
#     x = '*.gfeat'
    
    
if level == 'L3':
    for i in glob.glob(os.path.join(data, '*.gfeat', 'cope1.feat', 'rendered_thresh_zstat*.png')):
        print i
        dstpath = os.path.join(os.path.expanduser('~'), exp, 'Analysis', task, version, level, 'rendered')
        try: 
            os.makedirs(dstpath)
        except: 
            pass
        fid = i.split(os.sep)[-3].split('.')[0]+'_'+i.split(os.sep)[-1].split('.')[0][-1]+'.png'
        dst = os.path.join(dstpath, fid)
        shutil.copyfile(i,dst)

    for i in glob.glob(os.path.join(data, '*.gfeat', 'cope1.feat', 'rendered_thresh_zfstat*.png')):
        dstpath = os.path.join(os.path.expanduser('~'), exp, 'Analysis', task, version, level, 'rendered')
        try: 
            os.makedirs(dstpath)
        except: 
            pass
        fid = i.split(os.sep)[-3].split('.')[0]+'_FTEST_'+i.split(os.sep)[-1].split('.')[0][-1]+'.png'
        dst = os.path.join(dstpath, fid)
        shutil.copyfile(i,dst)

    for i in glob.glob(os.path.join(data, '*.gfeat', 'cope1.feat', 'rendered_thresh*.gz')):
        dstpath = os.path.join(os.path.expanduser('~'), exp, 'Analysis', task, version, level, 'thresh_zstat')
        try: os.makedirs(dstpath)
        except: pass
        fid = i.split(os.sep)[-3].split('.')[0]+'_'+i.split(os.sep)[-1].split('.')[0][-1]+'.nii.gz'
        dst = os.path.join(dstpath, fid)
        shutil.copyfile(i,dst)

    for i in glob.glob(os.path.join(data, '*.gfeat', 'cope1.feat', 'stats', 'zstat*.nii.gz')):
        dstpath = os.path.join(os.path.expanduser('~'), exp, 'Analysis', task, version, level, 'zstat')
        try: os.makedirs(dstpath)
        except: pass
        fid = i.split(os.sep)[-4].split('.')[0]  +'_'+ i.split(os.sep)[-1].split('.')[0][-1] + '.nii.gz'
        dst = os.path.join(dstpath, fid)
        shutil.copyfile(i,dst)
    