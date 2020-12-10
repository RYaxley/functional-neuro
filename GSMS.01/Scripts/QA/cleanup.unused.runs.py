#!/usr/bin/env python
# encoding: utf-8

import os
import shutil

model = 'LA.Simple'
runs = range(1,10)

f = file(os.path.expanduser('~/GSMS.01/Scripts/Subjects/subjects.py'))
exec(f)
f.close()
subjects = dict(subjects)

for subj, info in sorted(subjects.iteritems()):

    for run in runs:

        if info[run+3] == 0:

            fid = os.path.join('/Volumes/GSMS.01/Analysis/', model, 'Level.1', subj, str(run).zfill(2) + '.feat')

            if os.path.exists(fid):
                print fid

                os.listdir(fid)
                shutil.rmtree(fid)



