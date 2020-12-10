#!/usr/bin/env python
# encoding: utf-8

"""
EV.py

Creates EV files based on behavioral data.

Created by Richard Yaxley on 2010-02-05.
"""

import sys
import os
import glob
import scipy as S
             
             
study = 'CUD.01'

# Specify paths
# exp_remote = CUD.01 directory on Munin
# exp_local = Scripts directory in home directory
if os.getlogin() == 'richardyaxley': # Macbook
    exp_remote = os.path.join('/Volumes', study)
    exp_local = os.path.join(os.path.expanduser('~'), study)
elif os.getlogin() == 'yaxley': # Cluster node
    exp_remote = os.path.join(os.path.expanduser('~'),'experiments', study)
    exp_local = os.path.join(os.path.expanduser('~'), study)
elif os.getlogin() == 'sb212': # Cluster node
    exp_remote = os.path.join(os.path.expanduser('~'),'net', 'munin', 'data', 'debellis', study)
    exp_local = os.path.join(os.path.expanduser('~'), 'net', 'munin', 'data', 'debellis', study)    
opath = os.path.join(exp_local, 'Analysis', 'EV')

f = file(os.path.join(exp_local, 'Scripts', 'Subjects', 'subjects.py'))
exec(f)
f.close()
subjects = dict(subjects) 

          
def check_create_dir(path):
    """docstring for check_create_dir"""
    if not os.path.isdir(path):
        os.makedirs(path)   

        
def write_ev_file(evname, path, subj, sess, time, dur, weight):
    """Writes EV files in 3-column format for FSL.
    prefix =
    """                                                           
    # If empty EV, write zeros at timepoint 1
    if time.size == 0:
        # time = S.ones(1)
        # weight = dur = S.array([0])      
        time = weight = dur = S.array([0])    
    fid = os.path.join(path, subj)
    check_create_dir(fid)               
    fid = '.'.join([ str(sess).zfill(2), evname, 'txt' ])
    fid = os.path.join(path, subj, fid)
    f = open(fid, 'w')
    for row in range(time.size):
        print >> f, '%07.3f\t%5.3f\t%+06.3f' %(time[row], dur[row], weight[row])
    f.close() 



for subj, info in sorted(subjects.iteritems()):
    if subj == '31824':
        print 'skipping', subj
    
    else:
        # Adolescents
        if info[0] <= 3:
            tr = 2
        # Adults
        elif info[0] >= 4:
            tr = 1.5

        for i in glob.glob(os.path.join(exp_local, 'Data', 'Behavioral', subj, 'output_?????_?.txt')):
            sess = i.split(os.sep)[-1].split('.')[0][-1]          
            fid = open(i)
            f = fid.readlines()
            fid.close()       
                 
            data = []
            for line in f:       
                line = line.split()     
                line = [float(s) for s in line]   
                data.append(line)  
            data = S.array(data)     
                         
            # If first event occurred at 6 seconds, then disdaqs were removed at
            # scanner and behavioral files were adjusted accordingly. However,
            # if events started at 12 s, the behavioral files were not adjusted
            # for disdaq time. All of the Adults' fMRI data had 4 disdaqs
            # removed at the scanner, so we didn't need to remove any disdaqs
            # from the image files. However, the behavioral files were saved
            # differently for Adults E1 & E2: E1 events started @ 12 s. E2
            # events started @ 6 s. None of the kids had disdaqs removed at the
            # scanner except for #31700.
            if data[0,1] == 12000:
                disdaqs = 4
            elif data[0,1] == 6000:
                disdaqs = 0
            else:
                print 'Timing discrepancy. Check behav data for', subj, sess                

            # Correct timing for removed volumes
            data[:,1] = (data[:,1]/1000) - (disdaqs * tr)
            
            # print subj, 'Session:',sess, 'Disdaqs:', disdaqs, 'Event #1 (s):', data[0,1]
            
            # ÏNDEX EVENT TYPES
            # for events 2 & 4 need resp 1 ( or left)
            # for events 1 & 3 need resp 2 ( or right)
            # 7 is the outcome of a reward  ('$' or '$$')
            # 9 is the outcome of an error/no response ('X')
            # 8 is the outcome for predetermined no reward ('X')
            square = S.array(S.nonzero(data[:,0] == 1)).flatten()
            star = S.array(S.nonzero(data[:,0] == 2)).flatten()
            trapezoid = S.array(S.nonzero(data[:,0] == 3)).flatten()
            circle = S.array(S.nonzero(data[:,0] == 4)).flatten()
            triangle = S.array(S.nonzero(data[:,0] == 5)).flatten()
            prompt = S.array(S.nonzero(data[:,0] == 6)).flatten()
            reward = S.array(S.nonzero(data[:,0] == 7)).flatten()
            noreward = S.array(S.nonzero(data[:,0] == 8)).flatten()
            noresponse = S.array(S.nonzero(data[:,0] == 9)).flatten() 
            
            # Index acceptable response outcomes
            acceptable_outcome = S.union1d(reward, noreward)
            # Index acceptable responses based on outcomes
            acceptable_resp = acceptable_outcome - 1
            # Index acceptable stimuli based on outcomes
            acceptable_stim = acceptable_outcome - 2
                                            
            # Stimuli by condition (No Risk, Reward Risk, & Behavioral Risk)
            nr = S.union1d(square, star)
            rr = S.union1d(trapezoid, circle)
            br = triangle 
            stim = S.union1d(nr, rr)
            stim = S.union1d(stim, br) 
            
            # No Risk stimulus
            T = data[S.intersect1d(nr, acceptable_stim), 1] 
            D = S.ones(len(T))
            W = S.ones(len(T)) 
            write_ev_file('NR', opath, subj, sess, T, D, W)   
            
            T = data[nr, 1] 
            D = S.ones(len(T))
            W = S.ones(len(T)) 
            write_ev_file('NR.All', opath, subj, sess, T, D, W) 
            
            # Reward Risk stimulus  
            T = data[S.intersect1d(rr, acceptable_stim), 1] 
            D = S.ones(len(T))
            W = S.ones(len(T)) 
            write_ev_file('RR', opath, subj, sess, T, D, W)  
            
            T = data[rr, 1] 
            D = S.ones(len(T))
            W = S.ones(len(T)) 
            write_ev_file('RR.All', opath, subj, sess, T, D, W)             
            
            # Behavioral Risk stimulus
            T = data[S.intersect1d(br, acceptable_stim), 1]
            D = S.ones(len(T))
            W = S.ones(len(T)) 
            write_ev_file('BR', opath, subj, sess, T, D, W)  
            
            T = data[br, 1]
            D = S.ones(len(T))
            W = S.ones(len(T)) 
            write_ev_file('BR.All', opath, subj, sess, T, D, W)  
            
            # Stimulus events
            T = data[stim,1] 
            D = S.ones(len(T))
            W = S.ones(len(T))
            write_ev_file('Stim', opath, subj, sess, T, D, W)    

            # Rewarded outcomes         
            T = data[reward,1]
            D = S.ones(len(T))
            W = S.ones(len(T)) 
            write_ev_file('Reward', opath, subj, sess, T, D, W)     

            # Unrewarded outcomes         
            T = data[noreward,1]
            D = S.ones(len(T))
            W = S.ones(len(T)) 
            write_ev_file('NoReward', opath, subj, sess, T, D, W) 

            # Responses
            T = data[acceptable_resp, 1]
            D = S.ones(len(T))
            W = S.ones(len(T)) 
            write_ev_file('Resp', opath, subj, sess, T, D, W) 
            
            # No response
            T = data[noresponse-1, 1]
            D = S.ones(len(T))
            W = S.ones(len(T)) 
            write_ev_file('NoResp', opath, subj, sess, T, D, W)   
            
            # Outcome by condition 
            nr_r = S.intersect1d(reward, nr+2)       
            rr_r = S.intersect1d(reward, rr+2)
            rr_u = S.intersect1d(noreward, rr+2)       
            br_r = S.intersect1d(reward, br+2)
            br_u = S.intersect1d(noreward, br+2)       
                  
            # No Risk Rewarded Outcome
            T = data[nr_r,1]
            D = S.ones(len(T))
            W = S.ones(len(T)) 
            write_ev_file('NR_R', opath, subj, sess, T, D, W)     
            
            # Reward Risk Rewarded Outcome
            T = data[rr_r,1]
            D = S.ones(len(T))
            W = S.ones(len(T)) 
            write_ev_file('RR_R', opath, subj, sess, T, D, W)  
            
            # Reward Risk Unrewarded Outcome
            T = data[rr_u,1]
            D = S.ones(len(T))
            W = S.ones(len(T)) 
            write_ev_file('RR_U', opath, subj, sess, T, D, W)
            
            # Behavioral Risk Rewarded Outcome
            T = data[br_r,1]
            D = S.ones(len(T))
            W = S.ones(len(T)) 
            write_ev_file('BR_R', opath, subj, sess, T, D, W)  
            
            # Reward Risk Unrewarded Outcome
            T = data[br_u,1]
            D = S.ones(len(T))
            W = S.ones(len(T)) 
            write_ev_file('BR_U', opath, subj, sess, T, D, W)   
            
            # Index all Events for error checking
            all = S.union1d(stim, prompt)
            all = S.union1d(all, reward)
            all = S.union1d(all, noreward)
            all = S.union1d(all, noresponse)
            T = data[all,1]
            D = data[all,0] # S.ones(len(T))
            W = data[all,3] #S.ones(len(T)) 
            write_ev_file('All', opath, subj, sess, T, D, W)  
            
            
                   
                            
