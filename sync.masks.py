#!/usr/bin/env python
# encoding: utf-8
"""
sync.masks.py

Created by Richard Yaxley on 2010-04-12.

Copy specific MR images to directory to quickly view them.

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
    data = os.path.join(analysis, level, '0disdaqs')
    dstpath = os.path.join(os.path.expanduser('~'), 'Desktop', 'Masks', level, '0disdaqs')
else:
    data = os.path.join(analysis, task, version, level)
    dstpath = os.path.join(os.path.expanduser('~'), exp, 'Analysis', 'Masks', model, level)

try:
    os.makedirs(dstpath)
except:
    pass
    
if not os.path.isdir(data):
    print 'Data Unavailable: ', data    


if level != 'L3':
    for i in glob.glob(os.path.join(data, '?????', '*feat', 'mask.nii.gz')): 
        fid = i.split('/')[-3] + '.' + i.split('/')[-2][:2] + '.nii.gz'
        dst = os.path.join(dstpath, fid)
        shutil.copyfile(i,dst)

elif level == 'L3':
    if exp == 'CUD.01':
        fpath = os.path.join(data, '*gfeat', 'mask.nii.gz')
    elif exp == 'GSMS.01':
        fpath = os.path.join(data, '*','*gfeat', 'mask.nii.gz')
    for i in glob.glob(fpath): 
        fid = i.split(os.sep)[-2].split('.')[0] + '.nii.gz'
        dst = os.path.join(dstpath, fid)
        shutil.copyfile(i,dst)
    print 'Masks copied to:', 'file://'+os.path.split(dst)[0]
    
