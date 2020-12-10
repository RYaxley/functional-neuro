#!/usr/bin/env python
# encoding: utf-8
"""
check.ghosting.py

Created by Richard Yaxley on 2009-12-03.
"""

import os
import sys
import glob
import commands
import numpy as np
import time

model = 'Decision.100406'
task = model.split('.')[0]
version = model.split('.')[1]

data = os.path.join('/Volumes', 'CUD.01', 'Analysis', task, version)

for i in glob.glob(os.path.join(data, 'L1', '?????', '0?.feat')):
        
    fid = os.path.join(i, 'custom_timing_files', 'ev4.txt')
    f = open(fid, 'r')
    lines = f.readlines()
    f.close()
    
    subj = int(i.split(os.sep)[-2])

    # Here's the first timepoint of the Resp variable
    if version == '100406':
        if subj < 40000:
            testval = '007.000'
        elif subj < 43000:
            testval = '009.000'
        elif subj < 45000:
            testval = '009.000'
    elif version == '100401':
        if subj < 40000:
            testval = '015.000'
        elif subj < 43000:
            testval = '015.000'
        elif subj < 45000:
            testval = '009.000'
    
    if lines[0].split()[0] != testval:
        print i.split(os.sep)[-2:], '-', lines[0].split()[0]
        
        fid = os.path.join(i, 'custom_timing_files', 'ev5.txt')
        f = open(fid, 'r')
        lines = f.readlines()
        f.close()
        
        if lines[0].split()[0] == testval:
            print 'ok'



