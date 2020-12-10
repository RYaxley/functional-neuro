#!/usr/bin/env python
# encoding: utf-8

import sys
import os
import commands
import socket


'''
Sync data into respective directories.

'''

exp = sys.argv[1] # 'GSMS.01'
model = sys.argv[2] # 'PS.5disdaqs', 'TD.100311', Decision.100423
level = sys.argv[3] # 'PS', 'L1', 'L2', 'L3'


def syncBehavioral(local, remote):
    print '+ Behavioral Data'
    src = os.path.join(remote, 'Data', 'Behavioral')
    tgt = os.path.join(local, 'Data')
    cmd = 'rsync -%s %s %s' % (arg, src, tgt)
    output = commands.getoutput(cmd)
    
    



# Rsync arguments
arg = 'avz'

local = os.path.join(os.path.expanduser('~'), exp)
remote = os.path.join('/Volumes', exp)
print local, '--', remote

# See if remote directory exists. if not, mount drive
if os.path.isdir(remote):
    pass
else:
    print 'Remote drive not mounted.'

##   elif host == 'lse12lmbk1':
##
##       local = os.path.join(os.path.expanduser('~'), exp)
##       remote = os.path.join(os.path.expanduser('~'), 'Drives', exp)



                                          

#def syncNifti(local, remote):
#    print '+ NIFTI-formatted Data'
#    src = os.path.join(remote, 'Analysis', 'Images')
#    tgt = os.path.join(local, 'Analysis')
#    cmd = 'rsync -%s %s %s' % (arg, src, tgt)
#    output = commands.getoutput(cmd)
#
#def syncAnatomical(local, remote):
#    print '+ Anatomical data'
#    src = os.path.join(remote, 'Data', 'Anat')
#    tgt = os.path.join(local, 'Data')
#    cmd = 'rsync -%s %s %s' % (arg, src, tgt)
#    output = commands.getoutput(cmd)
#
#def syncFunctional(local, remote):
#    print '+ Functional data'
#    src = os.path.join(remote, 'Data', 'Func')
#    tgt = os.path.join(local, 'Data')
#    cmd = 'rsync -%s %s %s' % (arg, src, tgt)
#    output = commands.getoutput(cmd)
#
#
#def syncPrestats(local, remote):
#    print '+ Prestats'
#    src = os.path.join(remote, 'Analysis', 'PS','5disdaqs')
#    tgt = os.path.join(local, 'Analysis')
#    cmd = 'rsync -%s %s %s' % (arg, src, tgt)
#    output = commands.getoutput(cmd)           
#    
#def syncCondensedPrestats(local, remote):
#    print '+ Condensed Prestats'
#    src = os.path.join(remote, 'Analysis', 'PS', model.split('.')[1]+'/')
#    tgt = os.path.join(local, 'Analysis', 'Condensed', 'PS', model.split('.')[1]+'/')
#    try: 
#        os.makedirs(tgt)
#    except: 
#        pass
#    exc = "--exclude='*' "
#    inc = "--include='?????/' "
#    inc = inc + " --include='*/*.feat/' "
#    inc = inc + " --include='*/*.feat/report_log.html' "
#    inc = inc + " --include='*/*.feat/reg/' "
#    inc = inc + " --include='*/*.feat/reg/example_func2highres.png' "
#    inc = inc + " --include='*/*.feat/reg/example_func2standard.png' "
#    inc = inc + " --include='*/*.feat/reg/highres2standard.png' "
#    inc = inc + " --include='*/*.feat/mc/' "
#    inc = inc + " --include='*/*.feat/mc/*.png' "
#    cmd = 'rsync %s %s -%s %s %s' % (inc, exc, arg, src, tgt)
#    output = commands.getoutput(cmd)
#                  
#
#def syncL1(local, remote):
#    print '+ L1'
#    src = os.path.join(remote, 'Analysis', model, 'L1')
#    tgt = os.path.join(local,  'Analysis', model) 
#    cmd = 'rsync -%s %s %s' % (arg, src, tgt) 
#    output = commands.getoutput(cmd)  
#
#    
#def syncL2(local, remote):
#    print '+ L2'
#    src = os.path.join(remote, 'Analysis', model, 'L2')
#    tgt = os.path.join(local,  'Analysis', model) 
#    cmd = 'rsync -%s %s %s' % (arg, src, tgt) 
#    output = commands.getoutput(cmd)
#
#    
#def syncL3(local, remote):
#    print '+ L3'
#    src = os.path.join(remote, 'Analysis', model, 'L3')
#    tgt = os.path.join(local,  'Analysis', model) 
#    cmd = 'rsync -%s %s %s' % (arg, src, tgt) 
#    output = commands.getoutput(cmd)        
   

host = socket.gethostname().split('.')[0].lower()

#local, remote = setexpdirs(host, exp)
#
syncBehavioral(local, remote)

#syncNifti(local, remote)
#syncCondensedPrestats(local, remote)
# syncCondensedL3(local, remote)
#syncQA(local, remote)     
#syncL1(local, remote) 
#syncL2(local, remote)   
#syncL3(local, remote)       
#syncPrestats(local,remote)



