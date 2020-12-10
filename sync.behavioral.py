#!/usr/bin/env python
# encoding: utf-8

import sys
import os
import commands
import socket

    
exp = sys.argv[1] # "GSMS.01"

# Rsync arguments
arg = 'avz'

local = os.path.join(os.path.expanduser('~'), exp)
remote = os.path.join('/Volumes', exp)

# See if remote directory exists. if not, mount drive
if not os.path.isdir(remote):
    print 'Please mount experiment and try again.'
    pass
else:
    host = socket.gethostname().split('.')[0].lower()

    print '+ Behavioral Data'
    src = os.path.join(remote, 'Data', 'Behavioral')
    tgt = os.path.join(local, 'Data')
    cmd = 'rsync -%s %s %s' % (arg, src, tgt)
    output = commands.getoutput(cmd)
