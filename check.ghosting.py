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

regions = ('in3', 'out3')
subj = sess = brain = ghost =  []

data = os.path.join(os.path.expanduser('~'), 'GSMS.01', 'Data', 'FSL')

for i in glob.glob(os.path.join(data, '?????', '0?.nii.gz')):

    mask1 = os.path.join(data, regions[0] + '.nii.gz')
    mask2 = os.path.join(data, regions[1] + '.nii.gz')

    cmd = 'fslstats %s -k %s -M  -k %s -M' % (i, mask1, mask2)
    values = commands.getoutput(cmd).split()

    subj = np.append(subj, i.split('/')[-2])
    sess = np.append(sess, i.split('/')[-1][1])
    brain = np.append(brain, float(values[0]))
    ghost = np.append(ghost, float(values[1]))

    print '%d\t%d\t%0.0f\t%0.0f\t%0.1f' % (int(i.split('/')[-2]), int(i.split('/')[-1][1]), float(values[0]), float(values[1]), float(values[1])/float(values[0]) * 100)

#ratio = ghost/brain * 100
fid = os.path.join(data, 'ghosting.txt')
f = open(fid, 'w')
for i in range(subj.size):
    print >> f, '%d\t%d\t%0.0f\t%0.0f\t%0.1f' % \
    (subj[i].astype('int'), sess[i].astype('int'), brain[i], ghost[i], ghost[i]/brain[i] * 100)
f.close()


