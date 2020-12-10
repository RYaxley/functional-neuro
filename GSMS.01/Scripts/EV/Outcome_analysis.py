#!/usr/bin/env python
# encoding: utf-8
"""
LA_analysis.py

Created by Richard Yaxley on 2009-10-02.
"""

import sys
import os
import glob
import scipy as S
import scipy.io
import csv
import pylab as P
from operator import itemgetter

'''
This is the outcome phase of the the LA task. Each trial involves resolving one of the previously seen mixed gambles.
Each gamble has two amounts; a possible gain and a possible loss. The gamble is presented and then after a delay (X s) 
They then indicate their choice with a button press; 1 = accept, 2 = reject.
We want to extract the timing data for the onset of each trial.

need Stim    

need response
 
'''

def check_create_dir(path):
    """docstring for check_create_dir"""
    if not os.path.isdir(path):
        os.mkdir(path)


def get_subjects(path):
    """docstring for get_subjects"""
    fid = os.path.join(path, 'Subjects', 'subjects.py')
    f = open(fid)
    exec(f)
    f.close()
    return subjects

    
def write_ev_file(evname, path, subj, task, sess, time, dur, weight):
    """Writes EV files in 3-column format for FSL.
    prefix =
    """                                                           
    # If empty EV, write zeros
    if time.size == 0:
        # time = S.ones(1)
        time = weight = dur = S.array([0])        
    fid = os.path.join(path, subj)
    check_create_dir(fid)               
    fid = '.'.join([ task, str(sess).zfill(2), evname, 'txt' ])
    fid = os.path.join(path, subj, fid)
    f = open(fid, 'w')
    for row in range(time.size):
        print >> f, '%07.3f\t%5.3f\t%+05.2f' % (time[row], dur[row], weight[row])
    f.close()


def linear_transform(value, min, max, newmin, newmax):
    """docstring for lineartransform"""
    OldRange = (max - min)
    NewRange = (newmax - newmin)
    NewValue = (((value - min) * NewRange) / OldRange) + newmin
    return NewValue


exp_local = os.path.join(os.path.expanduser('~'), 'GSMS.01')
exp_remote = os.path.join('/Volumes', 'GSMS.01')
scripts = os.path.join(exp_local, 'Scripts')
idir = os.path.join(exp_remote, 'Data', 'Behavioral')
odir = os.path.join(exp_local, 'Analysis', 'EV')
check_create_dir(odir)
subjects = get_subjects(scripts) 
disdaqs = 5 # number of volumes to exclude
TR = 2 # sampling time
task = 'LA'

# Gain & loss amounts for entire range of values in all runs
Gains = S.arange(10,42,2)
Losses = S.arange(5,21) * -1

for subj, info in sorted(subjects.iteritems()):

    # Subject level data
    S_session = []
    S_trial = []
    S_resp = []
    S_gain = []
    S_loss = []

    for i in glob.glob(os.path.join(exp_local, 'Data', 'Behavioral', subj, task+'_?????_5.mat')):

        # Read .mat file and load the struct named 'data'
        fid = open(i)
        mat = S.io.loadmat(fid)
        fid.close()
        
        # Extract variables and convert 2-D arrays to 1-D vectors
        session = mat['data']['session'][0][0][0][0]
        trial = mat['data']['trial'][0][0][0]
        onset = mat['data']['onset'][0][0][0]
        RT = mat['data']['RT'][0][0][0]
        gain = mat['data']['gain'][0][0][0]
        loss = mat['data']['loss'][0][0][0]
        try:
            resp = mat['data']['resp'][0][0][0]
            pass
        except ValueError:
             resp = mat['data']['press'][0][0][0]

        # Shift time for discarded volumes
        onset = onset - disdaqs * TR

'''
        # Calculate onset for responses based on stimulus onset.
        resp_onset = onset + RT

        # Extract events and write EV files

        # Subject's choices
        responses = S.where(resp > 0)
        misses = S.where(resp == 0)
        accepted = S.where(resp == 1)
        rejected = S.where(resp == 2)

        # STIMULI
        # Trials subject responded to 
        T = onset[responses]
        D = S.ones(T.size)
        W = S.ones(T.size)
        write_ev_file('Stim', odir, subj, task, session, T, D, W)

        # Trials subject did not respond to
        T = onset[misses]
        D = S.ones(T.size)
        W = S.ones(T.size)
        write_ev_file('Miss', odir, subj, task, session, T, D, W)


        # RESPONSES
        # Response events
        T = resp_onset[responses]
        D = S.ones(T.size)   
        W = S.ones(T.size)
        write_ev_file('Resp', odir, subj, task, session, T, D, W)

        # Accepted gamble responses (unweighted)
        T = resp_onset[accepted]     
        D = S.ones(T.size)
        W = S.ones(T.size)
        write_ev_file('Accept', odir, subj, task, session, T, D, W)

        # Rejected gamble responses (unweighted)
        T = resp_onset[rejected]
        D = S.ones(T.size)
        W = S.ones(T.size)
        write_ev_file('Reject', odir, subj, task, session, T, D, W)


        # PARAMETRIC REGRESSORS
        # To model linear increase in activation as reward values increases.
        
        # Linear transformation of gain & loss ranges from 1 to -1
        GainScaled = []
        for i in gain:
            value = linear_transform(i.astype(float), Gains.min(), Gains.max(), -1, 1)
            GainScaled = S.append(GainScaled, value)
        LossScaled = []
        for i in loss:
            value = linear_transform(i.astype(float), Losses.max(), Losses.min(), -1, 1)
            LossScaled = S.append(LossScaled, value)

        # Gambles weighted by gain magnitude; duration = RT
        T = onset[responses]
        D = S.ones(T.size)
        W = GainScaled[responses]
        write_ev_file('Gain', odir, subj, task, session, T, D, W)

        # Gambles weighted by loss magnitude; duration = RT
        W = LossScaled[responses]
        write_ev_file('Loss', odir, subj, task, session, T, D, W)

'''