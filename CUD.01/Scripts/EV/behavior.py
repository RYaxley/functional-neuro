#!/usr/bin/env python
# encoding: utf-8

"""
Analysis of behavioral data.
"""

import sys
import os
import glob
import scipy as S
import scipy.stats
import csv
import pylab as P
from decimal import *
             
study = 'CUD.01'
exp_remote = os.path.join('/Volumes', study)
exp_local = os.path.join(os.path.expanduser('~'), study)   
opath = os.path.join(exp_local, 'Analysis', 'Behavior')

f = file(os.path.join(exp_local, 'Scripts', 'Subjects', 'subjects.py'))
exec(f)
f.close()
subjects = dict(subjects)

x = []
y = []
for subj, info in sorted(subjects.iteritems()):
    if info[0]==1: # or info[0]==4 or info[0]==5:
        
        data = []
        
        # Subject groups
        if info[0] == 1:
            group = 'CTRL'
        elif info[0] == 2:
            group = 'HR'
        elif info[0] == 3:
            group = 'CUD'
        elif info[0] == 4:
            group = 'ADLT'        
        elif info[0] >= 5:
            group = 'ADLT'
            
        for i in glob.glob(os.path.join(exp_local, 'Data', 'Behavioral', subj, 'output_?????_?.txt')):
            sess = i.split(os.sep)[-1].split('.')[0][-1]          
            fid = open(i)
            f = fid.readlines()
            fid.close()       

            for line in f:       
                line = line.split()     
                line = [Decimal(s) for s in line]  
                # print round(line[3],4)
                data.append(line)  
        data = S.array(data) 
            
        # Index event types      
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

        # Acceptable stim by condition
        nr_ok = S.intersect1d(acceptable_stim, nr)
        rr_ok = S.intersect1d(acceptable_stim, rr)
        br_ok = S.intersect1d(acceptable_stim, br)

        print 'nR: $', S.size(S.intersect1d(nr,reward-2)), 'X', S.size(S.intersect1d(nr,noreward-2))
        print 'RR: $', S.size(S.intersect1d(rr,reward-2)), 'X', S.size(S.intersect1d(rr,noreward-2))
        print 'BR: $', S.size(S.intersect1d(br,reward-2)), 'X', S.size(S.intersect1d(br,noreward-2))
        print '--'
        

        # RT by condition
        nr_rt = data[nr_ok+1, 3]
        rr_rt = data[rr_ok+1, 3]
        br_rt = data[br_ok+1, 3]

        nr_rt_avg = nr_rt.astype(float).mean()
        rr_rt_avg = rr_rt.astype(float).mean()
        br_rt_avg = br_rt.astype(float).mean()
            
        x.append([subj, group, 'NR', nr_rt_avg])
        x.append([subj, group, 'RR', rr_rt_avg])
        x.append([subj, group, 'BR', br_rt_avg])
        y.append([subj, group, nr_rt_avg, rr_rt_avg, br_rt_avg])
x = S.array(x)
y = S.array(y)


# Write all data to a text file
writer = csv.writer(open('behav_data.csv', 'w'), delimiter=',')
for i in y:
    writer.writerow(i)


# # Plot
# fig = P.figure()
# width = 0.3
# x1colors = '#c03000' # ['.9','.5','.2']
# x2colors = '#91aa9d' # ['1','.6','.3']
# x1label = 'Adolescents'
# x2label = 'Adults'
# x1 = []
# x2 = []
# x1e = []
# x2e = []
# x1loc = S.array(S.arange(1,4))
# x2loc = x1loc + width
for group in ['K','A']: # [1,2,3]:
    for cond in ['NR','RR','BR']:
        gidx = S.array(S.nonzero(x[:,0] == group)).flatten()
        cidx = S.array(S.nonzero(x[:,1] == cond)).flatten()
        data = x[S.intersect1d(gidx,cidx)][:,2].astype(float)
        xbar = S.stats.nanmean(data)
        xsem = S.std(data, ddof=1)/S.sqrt(len(data))
        if group == 'K':
            x1.append(xbar)
            x1e.append(xsem)
        elif group == 'A':
            x2.append(xbar)
            x2e.append(xsem)
        
P.bar(x1loc, x1, yerr=x1e, width=width, align='center', color=x1colors, ecolor='k', label=x1label)
P.bar(x2loc, x2, yerr=x2e, width=width, align='center', color=x2colors, ecolor='k', label=x2label)
P.title('Response times for Adolescents & Adults across levels of risk.')
P.ylabel('Mean Response Time (s)')
P.xlabel('Levels of Risk')
labels = 'NR RR BR'.split()
groups = 'Adolescents Adults'.split()
P.legend()
P.xlim(x1loc[0]-width, x2loc[-1]+width)
P.xticks(x1loc+width/2, labels)           
P.ylim(0,.6)
P.yticks(S.linspace(0,.6,7))
P.savefig(os.path.join(exp_local,'Documents','Manuscript','Figures','RT.png'))
# 
# # Display means
# print 'Kids'
# print([round(i,3) for i in x1])
# print 'Adults'
# print([round(i,3) for i in x2])