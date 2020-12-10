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
# import csv
# import pylab as P
# from operator import itemgetter

'''
In this experiment each trial involves the presentation of a mixed gamble.
Each gamble has two amounts; a possible gain and a possible loss. The
participants has to decide whether they want to accept or reject each gamble.
They then indicate their choice with a button press; 1 = accept, 2 = reject.
We want to extract the timing data for the onset of each trial.
'''

def check_create_dir(path):
    if not os.path.isdir(path):
        os.mkdir(path)


def get_subjects(path):
    fid = os.path.join(path, 'Subjects', 'subjects.py')
    f = open(fid)
    exec(f)
    f.close()
    return subjects

    
def write_ev_file(evname, path, subj, task, sess, time, dur, weight):
    """Writes EV files in 3-column format for FSL."""                                                           
    # If empty EV, write zeros
    if time.size == 0:
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
    OldRange = (max - min)
    NewRange = (newmax - newmin)
    NewValue = (((value - min) * NewRange) / OldRange) + newmin
    return NewValue



study = 'GSMS.01'
task = 'LA'
# exp_remote = CUD.01 directory on Munin
# exp_local = Scripts directory in home directory
if os.getlogin() == 'richardyaxley':
    location = 'MacBook'
    exp_remote = os.path.join('/Volumes', study)
    exp_local = os.path.join('/Volumes', study) #os.path.join(os.path.expanduser('~'), study)
elif os.getlogin() == 'yaxley':
    location = 'Cluster'
    exp_remote = os.path.join(os.path.expanduser('~'),'experiments', study)
    exp_local = os.path.join(os.path.expanduser('~'), 'experiments', study)
elif os.getlogin() == 'sb212': 
    location = 'Cluster'
    exp_remote = os.path.join(os.path.expanduser('~'),'net', 'munin', 'data', 'debellis', study)
    exp_local = os.path.join(os.path.expanduser('~'), 'net', 'munin', 'data', 'debellis', study)

scripts = os.path.join(exp_remote, 'Scripts')
idir = os.path.join(exp_remote, 'Data', 'Behavioral')
odir = os.path.join(exp_remote, 'Analysis', 'EV')

check_create_dir(odir)
subjects = get_subjects(scripts) 

disdaqs = 5 # number of volumes to exclude
TR = 2 # sampling time

rejectpoints = []

# Gain & loss amounts for entire range of values in all runs
Gains = S.arange(10,42,2)
Losses = S.arange(5,21) * -1

#---------------------------------------------------------------------------#
# Decision Runs
#---------------------------------------------------------------------------#
for subj, info in sorted(subjects.iteritems()):

    # Subject level data
    S_session = []
    S_trial = []
    S_resp = []
    S_gain = []
    S_loss = []

    for i in glob.glob(os.path.join(exp_remote, 'Data', 'Behavioral', subj, task+'_?????_[1234].mat')):
        
        # Read .mat file and load the struct named 'data'
        fid = open(i)
        mat = S.io.loadmat(fid)
        fid.close()

        # Extract variables and convert 2-D arrays to 1-D vectors
        if location == 'MacBook':
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
        elif location == 'Cluster':
            session = mat['data'].session
            trial = mat['data'].trial
            onset = mat['data'].onset
            RT = mat['data'].RT
            gain = mat['data'].gain
            loss = mat['data'].loss
            try:
                resp = mat['data'].resp
                pass
            except ValueError:
                 resp = mat['data'].press
            
        # Shift time for discarded volumes
        onset = onset - disdaqs * TR

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
        # D = S.ones(T.size) # duration = 1 s
        D = RT[responses] # duration = RT
        W = S.ones(T.size)
        write_ev_file('Stim', odir, subj, task, session, T, D, W)
        
        # Trials subject did not respond to
        T = onset[misses]
        D = S.ones(T.size)
        W = S.ones(T.size)
        write_ev_file('Miss', odir, subj, task, session, T, D, W)
        
        # RESPONSES
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
        # Gambles weighted by gain magnitude
        T = onset[responses]
        D = RT[responses] # duration = RT
        W = GainScaled[responses]
        write_ev_file('Gain', odir, subj, task, session, T, D, W)
        # Gambles weighted by loss magnitude
        W = LossScaled[responses]
        write_ev_file('Loss', odir, subj, task, session, T, D, W)

        # Concatenate all runs for each subject
        # subjtrial = S.append(subjtrial, trial)
        # subjresp = S.append(subjresp, resp)
        # subjgain = S.append(subjgain, gain)
        # subjloss = S.append(subjloss, loss)
        
        # Accepted gambles; weighted by gain magnitude; 1 s impulse
        if len(accepted[0]) > 0:
           time = onset[accepted]
           weight = GainScaled[accepted]
           dur = S.ones(len(time))
        else:
           time = weight = dur = S.array([0])
        #write_ev_file('AcceptGain', odir, subj, run, time, dur, weight)

        # Accepted gambles; weighted by loss magnitude; 1 s impulse
        if len(accepted[0]) > 0:
           time = onset[accepted]
           weight = LossScaled[accepted]
           dur = S.ones(len(time))
        else:
           time = weight = dur = S.array([0])
        #write_ev_file('AcceptLoss', odir, subj, run, time, dur, weight)

        # Rejected gambles; weighted by gain magnitude; 1 s impulse
        if len(rejected[0]) > 0:
           time = onset[rejected]
           weight = GainScaled[rejected]
           dur = S.ones(len(time))
        else:
           time = weight = dur = S.array([0])
        #write_ev_file('RejectGain', odir, subj, run, time, dur, weight)

        # Rejected gambles; weighted by loss magnitude; 1 s impulse
        if len(rejected[0]) > 0:
           time = onset[rejected]
           weight = LossScaled[rejected]
           dur = S.ones(len(time))
        else:
           time = weight = dur = S.array([0])
        #write_ev_file('RejectLoss', odir, subj, run, time, dur, weight)


        '''
        ### Categorize gambles into 4 bins (-1:1)
        bins = S.linspace(-1, 1, 5)
        bins[-1] = bins[-1] + .01 # nudge final value so it will be included
        GainBin = S.digitize(GainScaled, bins).astype('float')
        LossBin = S.digitize(LossScaled, bins).astype('float')
        
        # Categorize gambles into 16 cells (4X4)
        # Gain-Loss
        # 1-1, 2-1, 3-1, 4-1 => 01 02 03 04
        # 1-2, 2-2, 3-2, 4-2    05 06 07 08
        # 1-3, 2-3, 3-3, 4-3    09 10 11 12
        # 1-4, 2-4, 3-4, 4-4    13 14 15 16
        cell = []
        for g, l in zip(GainBin,LossBin):
           if g == 1:
               if l == 1:
                   cell = S.append(cell, '1')
               elif l == 2:
                   cell = S.append(cell, '5')
               elif l == 3:
                   cell = S.append(cell, '9')
               elif l == 4:
                   cell = S.append(cell, '13')
           elif g == 2:
               if l == 1:
                   cell = S.append(cell, '2')
               elif l == 2:
                   cell = S.append(cell, '6')
               elif l == 3:
                   cell = S.append(cell, '10')
               elif l == 4:
                   cell = S.append(cell, '14')
           elif g == 3:
               if l == 1:
                   cell = S.append(cell, '3')
               elif l == 2:
                   cell = S.append(cell, '7')
               elif l == 3:
                   cell = S.append(cell, '11')
               elif l == 4:
                   cell = S.append(cell, '15')
           elif g == 4:
               if l == 1:
                   cell = S.append(cell, '4')
               elif l == 2:
                   cell = S.append(cell, '8')
               elif l == 3:
                   cell = S.append(cell, '12')
               elif l == 4:
                   cell = S.append(cell, '16')
        cell = S.array(cell)


        ### Categorize best (cell 4) and worst (cell 13) gambles
        # Best = (gain: $34 to $40; loss:$5 to $8)
        # Worst = (gain: $10 to $16; loss: $17 to $20)
        best = S.nonzero(cell == '4')
        worst = S.nonzero(cell == '13')

        # Best gambles; unweighted
        if len(best) > 0:
           time = onset[best]
           weight = S.ones(len(time))
           dur = RT[best]
        else:
           time = weight = dur = S.array([0])
        write_ev_file('Best', odir, subj, run, time, dur, weight)

        # Worst gambles; unweighted
        if len(worst) > 0:
           time = onset[worst]
           weight = S.ones(len(time))
           dur = RT[worst]
        else:
           time = weight = dur = S.array([0])
        write_ev_file('Worst', odir, subj, run, time, dur, weight)


        ### Transform bin categories
        GainBin[S.nonzero(GainBin == 1)] = -1.0
        GainBin[S.nonzero(GainBin == 2)] = -0.5
        GainBin[S.nonzero(GainBin == 3)] = 0.5
        GainBin[S.nonzero(GainBin == 4)] = 1.0
        LossBin[S.nonzero(LossBin == 1)] = -1.0
        LossBin[S.nonzero(LossBin == 2)] = -0.5
        LossBin[S.nonzero(LossBin == 3)] = 0.5
        LossBin[S.nonzero(LossBin == 4)] = 1.0
        time = onset[hits]
        dur = RT[hits]
        weight = GainBin[hits]
        write_ev_file('GainBin', odir, subj, run, time, dur, weight)
        weight = LossBin[hits]
        write_ev_file('LossBin', odir, subj, run, time, dur, weight)
        
        '''



        ### Calculcate Gain/Loss ratio for each gamble

        # Tom et al used Logistic Regression:
        # We assessed behavioral sensitivity to gains and losses by fitting a logistic
        # regression to each participant’s acceptability judgments collected during
        # scanning, using the size of the gain and loss as independent variables. Based
        # on this analysis, we computed a measure of behavioral loss aversion l as the
        # ratio of the (absolute) loss response to the gain response, which yielded a
        # median l = 1.93 (range: 0.99 to 6.75). 
        subjtrial = S.arange(1, subjtrial.size + 1)
        subjaccept = S.nonzero(subjresp == 1)
        subjreject = S.nonzero(subjresp == 2)
        subjratio = subjgain/subjloss * -1

        # Sort subject's data by ratio
        # s = zip(subjratio, subjresp)
        # s = sorted(s, key = lambda x:(-x[0], x[1]))
        # subjratiosort = S.array(map(itemgetter(0), s))
        # subjrespsort = S.array(map(itemgetter(1), s))

        # Find first rejection (ie, resp == 2) and identify corresponding ratio
        # subjreject = S.nonzero(subjrespsort == 2)
        # firstreject = subjreject[0][5]
        # rejectpoint = subjratiosort[firstreject]
        # rejectpoints = S.append(rejectpoints, rejectpoint)

        ### How many trials does each ratio explain
        x = []
        for ratio in S.linspace(1, 8, 4):

               # identify all trials with real gamble ratio <= ratio
               ratioresp = subjresp[subjratio <= ratio]
               # Of these trials, how many were accepted (ie, resp == 1)
               ratiosum = ratioresp[ratioresp == 1].sum()
               ratioprop = ratiosum/subjtrial.size

               # keep track of how many trials are explained by each ratio
               print '%1d %3.0f %0.1f' % (ratio, ratiosum, ratioprop)


#---------------------------------------------------------------------------#
# Outcome Run
#---------------------------------------------------------------------------#
for subj, info in sorted(subjects.iteritems()):

   # Subject level data
   S_session = []
   S_trial = []
   S_resp = []
   S_gain = []
   S_loss = []

   for i in glob.glob(os.path.join(exp_remote, 'Data', 'Behavioral', subj, task+'_?????_5.mat')):
       print i





