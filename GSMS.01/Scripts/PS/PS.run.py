#!/usr/bin/env python

import os
import fnmatch
import time
import subprocess

home = os.path.expanduser('~')
exp = os.path.join(home, 'GSMS.01')
analysis = os.path.join(exp, 'Analysis', 'PS')

for name in os.listdir(analysis):

    if fnmatch.fnmatch(name, '*.fsf'):

        level, subject, run, ext = name.split('.')

        job = os.path.join(analysis, name)

        outdir = run + '.feat'
        outdir = os.path.join(analysis, subject, outdir)

        if not os.path.isdir(outdir):

            cmd = ['feat', job]
            subprocess.Popen(cmd).wait()

        #os.remove(job)
