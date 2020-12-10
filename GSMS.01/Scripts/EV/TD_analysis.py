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
In this experiment each trial involves the presentation of a two payouts. Each
payout has a scheduled time (e.g., Today vs 2 weeks). The participants has to
decide which payout they want. They then indicate their choice with a button
press. We want to extract the timing data for the onset of each trial.
 
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
    """Writes EV files in 3-column format for FSL.    """                                                           
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
task = 'TD'
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


G_K = []
# plotnum = 0
# P.figure(figsize=(16,10))

for subj, info in sorted(subjects.iteritems()):
    
    # Subject level data
    S_session = []
    S_trial = []
    S_resp = []
    S_RT = []
    S_M1 = []
    S_M2 = []
    S_D2 = []
    S_K = []
    
    
    for i in glob.glob(os.path.join(exp_local, 'Data', 'Behavioral', subj, task+'_?????_?.mat')):
        
        # Read .mat file and load the struct named 'data'
        fid = open(i)
        mat = S.io.loadmat(fid)
        fid.close()

        # Extract variables and convert 2-D arrays to 1-D vectors
        if location == 'MacBook':
            session = mat['data']['session'][0][0][0][0]
            trial = mat['data']['trial'][0][0][0]
            onset = mat['data']['onset'][0][0][0]
            resp = mat['data']['resp'][0][0][0]
            RT = mat['data']['RT'][0][0][0]
            M1 = mat['data']['money1'][0][0][0]
            M2 = mat['data']['money2'][0][0][0]
            D2 = mat['data']['delay2'][0][0][0]
        elif location == 'Cluster':
            session = mat['data'].session
            trial = mat['data'].trial
            onset = mat['data'].onset
            resp = mat['data'].resp
            RT = mat['data'].RT
            M1 = mat['data'].money1
            M2 = mat['data'].money2
            D2 = mat['data'].delay2
            
        # Round values
        onset = onset.round(3)
        RT = RT.round(3)
        M1 = M1.round(2)
        M2 = M2.round(2)
        # print subj, session, M1.min(), M1.max(),  M2.min(), M2.max()

        # Shift time for discarded volumes
        onset = onset - disdaqs * TR

        # Calculate onset for responses based on stimulus onset.
        resp_onset = onset + RT


        # Extract events and write EV files
        # Subject's choices
        responses = S.where(resp > 0)
        misses = S.where(resp == 0)
        SSR = S.where(resp == 1) # sooner reward
        LLR = S.where(resp == 2) # later reward

        # Trials subject responded to 
        T = onset[responses]
        D = RT[responses] # duration based on RT
        W = S.ones(T.size)
        write_ev_file('Stim', odir, subj, task, session, T, D, W)

        # Trials subject did not respond to
        T = onset[misses]
        D = S.ones(T.size)
        W = S.ones(T.size)
        write_ev_file('Miss', odir, subj, task, session, T, D, W)
        
        # Onset of subject's responses
        T = resp_onset[responses]
        D = S.ones(T.size)
        W = S.ones(T.size)
        write_ev_file('Resp', odir, subj, task, session, T, D, W)        

        
        # CHOICES
        # Stim associated with SSR choices. Weight = -1
        T = onset[SSR]
        D = RT[SSR]
        W = S.ones(T.size) * -1
        write_ev_file('SSR', odir, subj, task, session, T, D, W)
        
        # Stim associated with LLR choices. Weight = +1
        T = onset[LLR]
        D = RT[LLR]
        W = S.ones(T.size)
        write_ev_file('LLR', odir, subj, task, session, T, D, W)        
        
        # SSR choices
        T = resp_onset[SSR]
        D = S.ones(T.size)
        W = S.ones(T.size)
        write_ev_file('Resp.SSR', odir, subj, task, session, T, D, W)

        # LLR choices
        T = resp_onset[LLR]
        D = S.ones(T.size)
        W = S.ones(T.size)
        write_ev_file('Resp.LLR', odir, subj, task, session, T, D, W)


        # PARAMETRIC REGRESSORS
        # To model linear increase in activation as reward values increases.
        
        # Linear transformation of SSR & LLR ranges from 1 to -1
        SSRscaled = []
        for i in M1:
            value = linear_transform(i.astype(float), M1.min(), M1.max(), -1, 1)
            SSRscaled = S.append(SSRscaled, value)
        LLRscaled = []
        for i in M2:
            value = linear_transform(i.astype(float), M2.min(), M2.max(), -1, 1)
            LLRscaled = S.append(LLRscaled, value)


        # Stimulus events and the corresonding parametric regressors of SSR & LLR
        
        # SSR choices weighted by SSR magnitude
        T = onset[SSR]
        D = RT[SSR] # duration = RT
        W = SSRscaled[SSR]
        write_ev_file('SSR.Scaled', odir, subj, task, session, T, D, W)
        
        # LLR choices weighted by LLR magnitude
        T = onset[LLR]
        D = RT[LLR]
        W = LLRscaled[LLR]
        write_ev_file('LLR.Scaled', odir, subj, task, session, T, D, W)
        
#---------------------------------------------------------------------------#

        # Concatenate all data for each subject
        S_trial = S.concatenate((S_trial, trial))
        S_session = S.concatenate((S_session, (S.ones(trial.size) * session)))
        S_resp = S.concatenate((S_resp, resp))
        S_RT = S.concatenate((S_RT, RT))
        S_M1 = S.concatenate((S_M1, M1.round(2)))
        S_M2 = S.concatenate((S_M2, M2.round(2)))
        S_D2 = S.concatenate((S_D2, D2))
    S_sequence = range(1,len(S_trial)+1)
    S_data = zip(S_sequence, S_trial, S_resp, S_RT, S_M1, S_M2, S_D2, )
    S_data = S.array(S_data)

    # Calculate proportion of choices SSR and LLR choices
    # try:
    #     choice_SSR = S.size(S.where(S_data[:,2]==1))
    # except Exception, e:
    #     raise e
    # choice_LLR = S.size(S.where(S_data[:,2]==2))
    # no_choice =  S.size(S.where(S_data[:,2]==0))
    # proportion_SSR = round(float(choice_SSR)/(choice_SSR+choice_LLR),2)
    
    # Calculate mean RT for all and SSR and LLR choices
    # mean_RT = round(S.average(S_data[:,3]),3)
    # SSR_RT = round(S_data[S.where(S_data[:,2]==1),3].mean(),3)
    # LLR_RT = round(S_data[S.where(S_data[:,2]==2),3].mean(),3)
    # print subj,'Mean RT=', mean_RT, 'SSR RT=', SSR_RT, 'LLR RT=', LLR_RT
    
    # print 'Mean:', G_K[:,1].astype(float).mean().round(3)
    # print 'SD:', G_K[:,1].astype(float).std().round(3)
    # print 'Min:', G_K[:,1].astype(float).min()
    # print 'Max:', G_K[:,1].astype(float).max()
        
        
    # # Write concatenated data array to file
    # fid = '.'.join([ task, 'txt' ])
    # # fid = os.path.join(odir, subj, fid)
    # # check_create_dir(os.path.join(odir, subj))
    # fid = os.path.join(os.path.expanduser('~'), 'Desktop', subj+fid)
    # f = open(fid, 'w')
    # for row in S_data:
    #     print >> f,  row
    # f.close() 

    

#---------------------------------------------------------------------------#
    # Calculate which k-value best predicts behavior
    k_values = S.linspace(0.0,1.0,100)
    k_errors = []
    for k in k_values:
        errors = 0
        for trial in S_data:
            choice = trial[1]                    
            SSR = trial[2]
            LLR = trial[3]
            delay = trial[4]
    
            # Calculate the discounted value of the larger delayed amount
            # Hyperbolic Discounting Function: Subjective_Value = LLR/(1 + Discount_Parameter * Delay_In_Weeks) 
            Value = LLR/(1 + k * delay)
     
            # Is the SSR or LLR greater at this k-value?
            if SSR > Value:
                larger_reward = 1
            elif Value > SSR:
                larger_reward = 2
            
            # Did the subject choose the larger reward?
            if choice != 0 and choice != larger_reward:
                errors += 1
        k_errors.append(errors)
    k_errors = S.array(k_errors)
    
    # ---------------------------------------------------------------------------#
    # Extract which k-values best reflected the subject's choice preference
    fewest_errors = S.where(k_errors == k_errors.min())
    best_k = k_values[fewest_errors]
    mean_k = S.mean(best_k)
    # K values for each Subject
    G_K.append([info[13], subj, round(mean_k,4)])
    # 
    # # Write concatenated data array to file
    # fid = os.path.join(exp_local, 'Analysis', 'TD', 'GSMS.discount.csv')
    # f = open(fid, 'w')
    # print >> f, 'GSMS_ID, BIAC_ID, DiscountValue'
    # writer = csv.writer(f , delimiter=',')
    # for i in G_K:
    #     writer.writerow(i)
    # f.close()
'''
#---------------------------------------------------------------------------#
    # # Plot
    # plotnum += 1
    # # Subplot settings
    # P.subplot(10,10,plotnum)
    # P.subplots_adjust(hspace=.8,wspace=.3)
    # # Title and text
    # P.title(subj,fontsize=10)
    # # P.plot(k_errors, color='b')
    # barwidth = 0.02
    # P.bar(k_values, k_errors, align='center', color='k', linewidth=0, width=barwidth)
    # # X-axis settings
    # P.xlim(k_values[0]-barwidth, k_values[-1]+barwidth)
    # P.xticks(S.linspace(k_values[0], k_values[-1], 2), (round(k_values[0],2),round(k_values[-1],2)), fontsize=7)
    # # Y-axis settings
    # P.ylim(0, S_data[:,0].size)
    # P.yticks(S.linspace(0, S_data[:,0].size, 3), ('','.5',''), fontsize=7)
    # # Horizontal line
    # P.axhline(y=(S_data[:,0].size/2), color='0.5', linestyle=':', linewidth=1)
    # # Vertical line
    # for error in best_k: #fewest_errors[0][:]:
    #     P.axvline(x=error, linewidth=1, color='r', alpha=0.5)
    # # Text
    # P.text(k_values[0], 160, 'SSR:'+str(proportion_SSR)+highlight, fontsize=6)
    # P.text(k_values[0], 130, 'K:'+str(round(mean_k,3)), fontsize=6)
    # P.savefig(os.path.join(exp_local, 'Analysis', 'TD', 'k_values'), dpi=300)

# print '-----'
# G_K = S.array(G_K)
# print 'Mean:', G_K[:,1].astype(float).mean().round(3)
# print 'SD:', G_K[:,1].astype(float).std().round(3)
# print 'Min:', G_K[:,1].astype(float).min()
# print 'Max:', G_K[:,1].astype(float).max()
'''
