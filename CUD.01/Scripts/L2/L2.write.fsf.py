#!/usr/bin/env python
import sys
import os
import glob


model = sys.argv[1]


if model == 'Decision.100423':
    # Design matrix = Contrast # : EVs
    design = {'1':  ['1',      1, 0, 0, 0, 0],
              '2':  ['1',     -1, 0, 0, 0, 0],
              '3':  ['2',      0, 1, 0, 0, 0],
              '4':  ['2',      0,-1, 0, 0, 0],
              '5':  ['3',      0, 0, 1, 0, 0],
              '6':  ['3',      0, 0,-1, 0, 0],
              '7':  ['12',     1,-1, 0, 0, 0],
              '8':  ['12',    -1, 1, 0, 0, 0],
              '9':  ['13',     1, 0,-1, 0, 0],
              '10': ['13',    -1, 0, 1, 0, 0],
              '11': ['23',     0,-1, 1, 0, 0],
              '12': ['23',     0, 1,-1, 0, 0],
              '13': ['123',   -1,-1, 2, 0, 0],
              '14': ['123',    1, 1,-2, 0, 0],
             }
elif model == 'Outcome.100708':   
    design = {'1':  ['1',      1, 0, 0, 0, 0, 0],
              '2':  ['1',     -1, 0, 0, 0, 0, 0],
              '3':  ['2',      0, 1, 0, 0, 0, 0],
              '4':  ['2',      0,-1, 0, 0, 0, 0],
              '5':  ['3',      0, 0, 1, 0, 0, 0],
              '6':  ['3',      0, 0,-1, 0, 0, 0],
              '7':  ['4',      0, 0, 0, 1, 0, 0],
              '8':  ['4',      0, 0, 0,-1, 0, 0],
              '9':  ['5',      0, 0, 0, 0, 1, 0],
              '10': ['5',      0, 0, 0, 0,-1, 0],
              '11': ['12345',  2, 2,-3, 2,-3, 0],
              '12': ['12345', -2,-2, 3,-2, 3, 0],
              '13': ['12',    -1, 1, 0, 0, 0, 0],
              '14': ['12',     1,-1, 0, 0, 0, 0],
              '15': ['24',     0, 1, 0,-1, 0, 0],
              '16': ['24',     0,-1, 0, 1, 0, 0],
              '17': ['23',     0, 1,-1, 0, 0, 0],
              '18': ['23',     0,-1, 1, 0, 0, 0],
              '19': ['45',     0, 0, 0, 1,-1, 0],
              '20': ['45',     0, 0, 0,-1, 1, 0],
              '21': ['14',     1, 0, 0,-1, 0, 0],
              '22': ['14',    -1, 0, 0, 1, 0, 0],
              '23': ['2345',   0, 2,-2, 2,-2, 0],
              '24': ['2345',   0,-2, 2,-2, 2, 0],
              '25': ['6',      0, 0, 0, 0, 0, 1],
              '26': ['6',      0, 0, 0, 0, 0,-1],
             } 

 
#############################################################################         
study = 'CUD.01'    
fsf = 'L2.fsf' 
task = model.split('.')[0]
version = model.split('.')[1]

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
    exp_local = os.path.join(os.path.expanduser('~'), study)



# data = os.path.join(exp_remote, 'Analysis', 'Images')
scripts = os.path.join(exp_local, 'Scripts') 
L1 = os.path.join(exp_remote, 'Analysis', task, version, 'L1')
L2 = os.path.join(exp_local, 'Analysis', task, version, 'L2')    
try:
    os.mkdir(L2)
except OSError:
    pass   
        
try:
    os.mkdir(os.path.join(scripts, 'L2', 'FSF'))
except OSError:
    pass 
             
                         
contrasts = range(1, len(design)+1)
copes = range(1, len(design['1']))
          
# Load subjects
fid = os.path.join(exp_remote, 'Scripts', 'Subjects', 'subjects.py')
f = file(fid)
exec(f)
f.close()
subjects = dict(subjects)   


if task == 'LA':
    firstrun = 1
    lastrun = 5
elif task == 'TD':
    firstrun = 5
    lastrun = 9
elif task == 'LA.outcome':
    firstrun = 9
    lastrun = 9
elif task == 'Decision':
    firstrun = 1
    lastrun = 6
elif task == 'Outcome':
    firstrun = 1
    lastrun = 6

for subject, info in sorted(subjects.iteritems()):      
    if info[0]:  
        for contrast, cope in sorted(design.iteritems()): 
              
            subjectpath = os.path.join(L1, subject)
            copelist = []           
            
            for used in info[firstrun:lastrun+1]: 
                if used:   
                    featdir = os.path.join(subjectpath, str(used).zfill(2)+'.feat') 
                    empty = False

                    for i in cope[0]:       
                        fid = os.path.join(featdir, 'tsplot', 'ps_tsplot_zstat1_ev'+str(i)+'.txt')
                        if not os.path.exists(fid):  
                            empty = True              
                    if not empty:
                        copelist.append(os.path.join(featdir, 'stats', 'cope'+contrast))   

            if len(copelist) > 1:  
            
                # Read .fsf template
                fid = open(fsf)
                template = fid.read()
                fid.close()  
            
                # Substitutions
                output = os.path.join(L2, subject.split('/')[-1], contrast.zfill(2))
                volumes = str(len(copelist))
                
                subs = {'set fmri(outputdir) "' : 'set fmri(outputdir) "' + output,
                        'set fmri(npts) 6' : 'set fmri(npts) ' + volumes,
                        'set fmri(multiple) 6' : 'set fmri(multiple) ' + volumes,
                       }
                for old, new in subs.iteritems():
                    template = template.replace(old, new)
                
                for i in range(len(copelist)):
                    old = 'set feat_files('+str(i+1)+') ""'
                    new = 'set feat_files('+str(i+1)+') "'+copelist[i]+'"'
                    template = template.replace(old, new)
                
                # Write new .fsf template
                fid = os.path.join(exp_local, 'Scripts', 'L2', 'FSF', model+'.'+subject.split('/')[-1]+'.'+str(contrast.zfill(2)))
                fid = '.'.join([fid, 'fsf'])
                f = file(fid, 'w')
                f.write(template)
                f.close()     
                fid = os.path.join(exp_remote, 'Scripts', 'L2', 'FSF', model+'.'+subject.split('/')[-1]+'.'+str(contrast.zfill(2)))
                fid = '.'.join([fid, 'fsf'])
                f = file(fid, 'w')
                f.write(template)
                f.close()  
