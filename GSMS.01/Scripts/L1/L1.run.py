#!/usr/bin/env python

import os
import fnmatch
import time
import subprocess
import glob

# Read in system arguments
#model = sys.argv[1]
model = 'LA/100309'

exp = os.path.join(os.path.expanduser('~'), 'GSMS.01')
jobpath = os.path.join(exp, 'Scripts', 'L1', 'FSF')


for i in sorted(glob.glob(os.path.join(jobpath, '*.fsf'))):

    info = i.split('/')
    fsf = info[-1]
    level = info[-3]

    opath = os.path.join(exp, 'Analysis', model, 'L1', fsf.split('.')[0], fsf.split('.')[1] + '.feat')
    if not os.path.isdir(opath):

        cmd = ['feat', i]
        subprocess.Popen(cmd).wait()

    #os.remove(job)
