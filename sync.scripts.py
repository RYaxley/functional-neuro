#!/usr/bin/env python
# encoding: utf-8
"""
sync.scripts.py

Created by Richard Yaxley on 2010-03-10.
"""

import os
import sys
import commands

username = 'yaxley'
arg = 'avz' # Rsync arguments
    
# Sync Generic Scripts 
print '+ Uploading General Scripts to ~/Scripts on cluster'
src = os.path.join(os.path.expanduser('~'), 'Scripts/')
tgt = username+'@hugin.biac.duke.edu:~/Scripts'
cmd = 'rsync -e ssh -%s --delete %s %s' % (arg, src, tgt)
output = commands.getoutput(cmd)    

# Sync Experiment Scripts
if not sys.argv[1]:
    print 'Please specify experiment directory and try again.'
    pass
else:
    exp = sys.argv[1]
    print exp
    
    print '+ Uploading ' + exp + ' Scripts to', exp, 'directory on cluster'    
    src = os.path.join(os.path.expanduser('~'), exp, 'Scripts')
    
    
    # Sync to Experiment directory
    tgt = os.path.join('/Volumes', exp)
    cmd = 'rsync -%s --delete %s %s' % (arg, src, tgt)
    output = commands.getoutput(cmd)    
    print output

    # Sync to Hugin Cluster
    tgt = 'yaxley@hugin.biac.duke.edu:~/' + exp
    cmd = 'rsync -e ssh -%s --delete %s %s' % (arg, src, tgt)
    output = commands.getoutput(cmd)