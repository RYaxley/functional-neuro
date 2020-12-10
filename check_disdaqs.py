#!/usr/bin/env python
# encoding: utf-8
"""
check_disdaqs.py

Created by Richard Yaxley on 2010-04-26.
"""

import sys
import os
import glob
import commands
import subprocess
import re

# This is my modified version of DVS's check_disdaqs.sh script. This
# script extracts the scan duration from the .pfh files and compares the
# durateion with the number of volumes actually recorded.

exp = 'CUD.01'
TR = 1.5 #2.0

data = os.path.join('/Volumes', exp, 'Data', 'Func')
opath = os.path.join('/Volumes', exp, 'Analysis', 'Pfile')
try: 
    os.mkdir(opath)
except OSError: 
    pass
    

for i in glob.glob(os.path.join(data, '*_?????', 'run00*', 'run00*.pfh')):
    ofile =  os.path.join(os.path.join(opath, 
             i.split(os.sep)[-3][-5:] + '_' + i.split(os.sep)[-2][-2:]) + '.txt')
    cmd = 'home/gadde/anonymizers/printpfileheader.pl ' + i + ' > ' + ofile
    os.system(cmd)
    
    f = open(ofile)
    file = f.read()
    f.close()
    file = file.splitlines()

    # Extract number of timepoints from Pfile
    scanduration = 0.0
    pattern = 'MR_sctime'
    for line in file:
        if re.search(pattern, line):
            try:
                scanduration = line.split()[3][1:4]
                scanduration = float(scanduration)
            except:
                print i
    
    # Look for actual # of volumes collected
    volumes = 0
    for j in glob.glob(os.path.join(os.path.dirname(i), 'V0???.img')):
        volumes += 1
    expectedduration = volumes * TR
    
    if expectedduration != scanduration:
        print 'ERROR: Scan duration:', scanduration, 'does not equal expected:', expectedduration, 'for ', i.split(os.sep)[-3:-1]
    
    
    
    
    