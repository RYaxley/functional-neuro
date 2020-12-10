#!/usr/bin/env python
# encoding: utf-8
"""
FQ.py

Reads, organizes, and plots FeatQuery output.

Created by Richard Yaxley on 2010-02-05.

"""

import sys
import os         
import glob
import subprocess     
import scipy as S
import scipy.stats as SS
import pylab as P
from xlwt import Workbook

#---------------------------------------------------------------------------#
# Decision
#model = 'Decision.100423'
#contrasts = [1,3,5]
#labels = ['NR', 'RR', 'BR' ]

# groups = ['CTRL', 'HR','CUD'] 
# February 2, 2011
# roi = '13_9_posterior' 
# title = 'Superior parietal lobule'
# February 10, 2011
# roi = 'Males+Age_13_9_ACC' 
# title = 'Males+Age_13_9_ACC'
# roi = 'Males+Age_13_9_Parietal' 
# title = 'Males+Age_13_9_Parietal'

# Controls + Adults Paper
groups = ['CTRL']
grouplabels = ['Adolescents']
# CTRL + Males - February 28, 2011
# roi = 'CTRL_13_1_ACC'
# title = 'ACC'
# roi = 'CTRL_13_1_FP'
# title = 'Frontal Pole'

# CTRL + Males
# roi = 'ACC+'
# title = 'ACC'
# roi = 'fp'             
# title = 'Frontal Pole'

# roi = 'pcuneus'             
# title = 'Precuneus'
# roi = '9_3_acc'             
# title = '9_3_acc'
# roi = '9_3_thal'             
# title = '9_3_thal'
# roi = '11_4_acc'             
# title = '11_4_acc'
# roi = '11_4_pcun'             
# title = '11_4_pcun'

#---------------------------------------------------------------------------#
# Outcome
model = 'Outcome.100708'
contrasts = [1,3,5,7,9]  
labels = ['NR/$', 'RR/$', 'RR/X', 'BR/$', 'BR/X' ]

# March 3, 2011
roi = 'CTRL_23_1_Accumbens'
title = 'Accumbens'

# February 8, 2011
# roi = '11_8_caudate'
# title = 'Caudate'
# roi = '23_8_fpole'
# title = 'Frontal pole'

# February 10, 2011
# roi = 'Males+Age_23_7_PCC' 
# title = 'Males+Age_23_7_PCC'

# 2 Group: Controls + Adults
# roi = 'vstriatum'
# roi = 'vstr'
# roi = 'dstr'
# roi = 'Accumbens'
# title = 'Accumbens'

# 3 Group: CTRL, HR, CUD
# roi = 'males_ftest_23_pcc'
# roi = 'males_ftest_11_pcc'
# roi = 'males_ftest_11_vmpfc'
# roi = '23_8_fpole'
# title = 'fpole'
#---------------------------------------------------------------------------#

study = 'CUD.01'                
task = model.split('.')[0]
version = model.split('.')[1]
exp_remote = os.path.join('/Volumes', study)
exp_local = os.path.join(os.path.expanduser('~'), study)
scripts = os.path.join(os.path.join(exp_local, 'Scripts'))
ROI =  os.path.join(exp_remote, 'Analysis', task, version, 'ROI')

# Load subject list
exec(file(os.path.join(scripts, 'Subjects', 'subjects.py')))
subjects = dict(subjects)

# Reduce subject's data and remove unused subjects from dictionary
for i, j in sorted(subjects.iteritems()):
    # Exclude unused subjects
    if j[10] == 'N': 
        del subjects[i] 
    # Reduce data
    elif j[0]: 
        del j[10]
        del j[1:9]

# Read data for each subject & contrast, if it exists.
for contrast in contrasts: 
    for subject, info in sorted(subjects.iteritems()):
        fid = os.path.join(ROI, subject, str(contrast).zfill(2), roi, 'report.txt')
        try:
            f = open(fid)
            x = f.readlines()   
            f.close()     
            signal = float(x[0].split()[5]) # Mean percent signal change
            subjects[subject].append(signal)
        except:
            subjects[subject].append(S.nan)
            if subject < '40000':
                print 'missing', subject, contrast  # Adolescents who are missing FQ data
            pass

# Reorganize data into array                                    
data = []
count = 1
for contrast in contrasts: 
    count += 1
    for subject, info in sorted(subjects.iteritems()):  
        group = int(info[0]) 
        # Lump all Adult Ps into the same group
        if group >= 4: group = 4
        signal = float(info[count])
        data.append([contrast, group, signal]) 
data = S.array(data)    

if task == 'Decision':

    print 'Plotting Decision'
    P.figure()  
    titlecount = 0
    plotcount = 1

    for group in groups:
        if group == 'CTRL':
            groupnum = 1
        elif group == 'HR':
            groupnum = 2
        elif group == 'CUD':
            groupnum = 3
        elif group == 'ADLT':
            groupnum = 4
            
        d = []
        e = []
        
        for contrast in contrasts:
            contrastidx = S.flatnonzero(data[:,0] == contrast)
            groupidx = S.flatnonzero(data[:,1] == groupnum)
            idx = S.intersect1d(contrastidx, groupidx)
            x = data[idx,2]
            xbar = S.stats.nanmean(x)
            xerr = S.stats.nanstd(x)/S.sqrt(len(x))
            d.append(xbar)
            e.append(xerr)

        P.subplot(1,S.size(groups),plotcount)
        P.axhline(y=0, linewidth=1, color='k') # Horizontal line at y=0
        xlocations = S.array(range(1,len(d)+1))
        P.bar(xlocations, d, yerr=e, width=0.5, align='center', color=['1.','.6','.3'], ecolor='k')
        if S.size(grouplabels) > 1:
            P.title(grouplabels[titlecount])
        P.xlim(0, xlocations[-1]+1)
        P.xticks(xlocations, labels)           
        P.ylim(0,.25)
        P.yticks(S.linspace(0,.25,6))
        P.subplots_adjust(hspace=.3)
        P.suptitle(title, fontsize=16, horizontalalignment = 'center', verticalalignment = 'top')
        P.savefig(os.path.join(ROI, '!Plots', title))
        titlecount += 1
        plotcount += 1
        
        # Reorganize data for new file
        z = []
        for subject, info in sorted(subjects.iteritems()):  
            group = int(info[0])    
            if group >= 4: group = 4
            z.append([subject, info[1], group, info[2], info[3], info[4]])
        z = S.array(z)
        # Write reorganized data to .csv file
        f = open(os.path.join(ROI, '!Plots', title+'.csv'), 'w')
        f.write('"{0}","{1}","{2}","{3}","{4}","{5}"\n'.format('ID#', 'HB#', 'GRP', 'NR', 'RR', 'BR'))
        for row in range(z[:,0].size):
            f.write('{0},{1},{2},{3},{4},{5}\n'.format(z[row,0], z[row,1], z[row,2], z[row,3], z[row,4], z[row,5]))
        f.close()
        
elif task == 'Outcome':

    print 'Plotting Outcome'
    P.figure()
    titlecount = 0
    plotcount = 1
    z = []
    
    for subject, info in sorted(subjects.iteritems()):  
        group = int(info[0])    
        if group >= 4: group = 4
            
    for group in groups:
        if group == 'CTRL':
            groupnum = 1
        elif group == 'HR':
            groupnum = 2
        elif group == 'CUD':
            groupnum = 3
        elif group == 'ADLT':
            groupnum = 4

        d = []
        e = []

        for contrast in contrasts:
            
            contrastidx = S.flatnonzero(data[:,0] == contrast)
            groupidx = S.flatnonzero(data[:,1] == groupnum)
            idx = S.intersect1d(contrastidx, groupidx)
            x = data[idx,2]
            xbar = S.stats.nanmean(x)
            xerr = S.stats.nanstd(x)/S.sqrt(len(x))
            d.append(xbar)
            e.append(xerr)   

            P.subplot(1,S.size(groups),plotcount)
            P.axhline(y=0, linewidth=1, color='k') # Horizontal line at y=0
            xlocations = S.array(range(1,len(d)+1))
            P.bar(xlocations, d, yerr=e, width=0.7, align='center', color=['1.','1.','.6','1.', '.6'], ecolor='k')
            if S.size(grouplabels) > 1:
                P.title(grouplabels[titlecount])
            P.xlim(0, xlocations[-1]+1)
            P.xticks(xlocations,  ['NR/$', 'RR/$', 'RR/X', 'BR/$', 'BR/X'])           
            P.ylim(-.1,.1)
            P.yticks(S.linspace(-.1,.1,5))
            # P.subplots_adjust(hspace=.3)
            P.suptitle(title, fontsize=16, horizontalalignment = 'center', verticalalignment = 'top')
            P.savefig(os.path.join(ROI, '!Plots', title))
            # titlecount += 1
            # plotcount += 1
    
        # Reorganize data for new file
        for subject, info in sorted(subjects.iteritems()):  
            group = int(info[0])    
            if group >= 4: group = 4
            z.append([subject, info[1], group, info[2], info[3], info[4], info[5], info[6]])
    z = S.array(z)
    # Write reorganized data to .csv file
    f = open(os.path.join(ROI, '!Plots', title+'.csv'), 'w')
    f.write('"{0}","{1}","{2}","{3}","{4}","{5}","{6}","{7}"\n'.format('ID#', 'HB#', 'GRP', 'NR/$', 'RR/$', 'RR/X', 'BR/$', 'BR/X'))
    for row in range(z[:,0].size):
        f.write('{0},{1},{2},{3},{4},{5},{6},{7}\n'.format(z[row,0], z[row,1], z[row,2], z[row,3], z[row,4], z[row,5], z[row,6], z[row,7]))
    f.close()
    
    # Reorganize difference score data into array
    diffscores = []
    for subject, info in sorted(subjects.iteritems()):  
        rr_r = info[2]
        rr_u = info[3]
        br_r = info[4]
        br_u = info[5]
        rr_diff = float(rr_r - rr_u)
        br_diff = float(br_r - br_u)
        diffscores.append([subject, group, rr_diff, br_diff])
    diffscores = S.array(diffscores)

    # Write reorganized data to file
    f = open(os.path.join(ROI, '!Plots', title+'.dat'), 'w')
    # f.write('"{0}","{1}","{2}","{3}","{4}"\n'.format('ID#', 'HB#', 'GRP', 'RR$', 'BR$'))
    # for row in range(diffscores[:,0].size):
    #     f.write('{0},{1},{2},{3}\n'.format(diffscores[row,0], diffscores[row,1], diffscores[row,2], diffscores[row,3]))
    # f.close()
    # 
    # # Write reorganized data to file #2
    # f = open(os.path.join(ROI, '!Plots', title+'_anova.csv'), 'w')
    # f.write('"{0}","{1}","{2}","{3}"\n'.format('ID', 'GRP', 'COND', 'SCORE'))
    # for row in range(diffscores2[:,0].size):
    #     f.write('{0},{1},{2},{3}\n'.format(diffscores2[row,0], diffscores2[row,1], diffscores2[row,2], diffscores2[row,3]))
    # f.close()

    '''
    
    # Plot
    
    # 3 group plot of Reward Difference scores for all 3 Adolescent groups
    if S.size(groups == 3):
        
        # Plot
        P.figure(figsize=(10.5,8))  
        titlecount = 0
        plotcount = 1

        for group in groups:
            if group == 'CTRL':
                groupnum = 1
            elif group == 'HR':
                groupnum = 2
            elif group == 'CUD':
                groupnum = 3
            d = []
            e = []
        
            for cond in [2,3]:
                groupidx = S.flatnonzero(diffscores[:,1] == str(groupnum))
                print groupidx
                x = diffscores[groupidx,cond].astype(float)
                xbar = S.stats.nanmean(x)
                xerr = S.stats.nanstd(x)/S.sqrt(len(x))
                d.append(xbar)
                e.append(xerr)
            print d
            P.subplot(1,3,plotcount)
            P.axhline(y=0, linewidth=1, color='k') # Horizontal line at y=0
            xlocations = S.array(range(1,len(d)+1))
            P.bar(xlocations, d, yerr=e, width=0.7, align='center', color=['1.','.6','.3'], ecolor='k')
            P.title(groups[titlecount])
            P.xlim(0, xlocations[-1]+1)
            P.xticks(xlocations,  ['RR/$', 'BR/$'])           
            ylimit = .25
            P.ylim(-ylimit,ylimit)
            P.yticks(S.linspace(-ylimit,ylimit,6))
            P.subplots_adjust(hspace=.3)
            P.suptitle(title, fontsize=16, horizontalalignment = 'center', verticalalignment = 'top')
            P.savefig(os.path.join(ROI, '!Plots', title+'_CTRL+HR+CUD'))
            titlecount += 1
            plotcount += 1


'''     