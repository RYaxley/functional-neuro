#! /usr/bin/env python
## 
## untitled
## 
## Created by Richard Yaxley on 2010-09-28.
## 

"""
Generates unique ROI mask for a figure.
"""
import os
import sys
import numpy as N
import scipy as S
import matplotlib as M
import matplotlib.pylab as P
from nifti import *

# Open standard brain template
fid = os.path.join(os.path.expanduser('~'),'CUD.01', 'Documents', 'Graphics', 'Parcellation','MNI152_T1_2mm_brain') # 'rotated_ch256'
image = NiftiImage(fid)
  
empty = image.copy()
empty.data[:] = 0.
mask = empty.copy()

# 16 ROIs
# Superior
# L   R
# 04  02
# 08  06
# 12  10
# 16  14
# Inferior
# L   R
# 03  01
# 07  05
# 11  09
# 15  13

# Calculate slope of horizontal plane
# Anterior Commissure (x = y-axis, y = z-axis)
x1 = 70.
y1 = 37.
# Posterior Commissure
x2 = 48.
y2 = 37.
# Slope: rise/run
m = (y1-y2)/(x1-x2)
# Y-intercept: y = mx + b
b = y1 - (m * x1)
plane = []
for x in range(mask.extent[1]+1):
    y = (m * x) + b
    y = int(N.round(y))
    plane.append(y)
S.array(plane)

# Inferior-to-Superior, Posterior-to-Anterior, Right-to-Left
xdim = range(mask.extent[2])
ydim = range(mask.extent[1])
zdim = range(mask.extent[0])

midline = 45

# Draw ROIs             
# intensity = S.array([5,9,8,13,
#                      3,10,7,14,
#                      2,11,6,15,
#                      1,12,5,16])

#   ant
#    |
# rt - lt
#    |
#   pos

# Both hemispheres
# intensity = S.array([4.9, 10.0, 9.0, 13.3,
#                      3.5, 10.8, 8.0, 14.1,
#                      2.0, 11.9, 7.0, 15.1,
#                      1.0, 12.6, 6.0, 16.0])

# Right
# ant1 = 83
# ant2 = 62
# post1 = 40
# post2 = 0
# intensity = S.array([4.9, 10.0, 0, 0,
#                      3.5, 10.8, 0, 0,
#                      2.0, 11.9, 0, 0,
#                      1.0, 12.6, 0, 0])
                     
# Left
ant1 = 82
ant2 = 62
post1 = 41
post2 = 0
intensity = S.array([0, 0, 9.0, 13.3,
                     0, 0, 8.0, 14.1,
                     0, 0, 7.0, 15.1,
                     0, 0, 6.0, 16.0])                     
                     
for x in xdim:
    for yslice in range(mask.extent[1]):
        top = range(int(plane[yslice])+1, mask.extent[0])
        bot = range(0, int(plane[yslice]))
        if yslice > ant1:
            if x < midline:
                mask.data[top, yslice, x] = intensity[0]
                mask.data[bot, yslice, x] = intensity[1]
            elif x > midline:
                mask.data[top, yslice, x] = intensity[2]
                mask.data[bot, yslice, x] = intensity[3]
        elif yslice < ant1 and yslice > ant2:
            if x < midline:
                mask.data[top, yslice, x] = intensity[4]
                mask.data[bot, yslice, x] = intensity[5]
            elif x > midline:
                mask.data[top, yslice, x] = intensity[6]
                mask.data[bot, yslice, x] = intensity[7]
        elif yslice < ant2 and yslice > post1:
            if x < midline:
                mask.data[top, yslice, x] = intensity[8]
                mask.data[bot, yslice, x] = intensity[9]
            elif x > midline:
                mask.data[top, yslice, x] = intensity[10]
                mask.data[bot, yslice, x] = intensity[11]
        elif yslice < post1 and yslice > post2:
            if x < midline:
                mask.data[top, yslice, x] = intensity[12]
                mask.data[bot, yslice, x] = intensity[13]
            elif x > midline:
                mask.data[top, yslice, x] = intensity[14]
                mask.data[bot, yslice, x] = intensity[15]


# Read mask to exclude regions
fid = os.path.join(os.path.expanduser('~'),'CUD.01','Documents','Graphics','Parcellation','rotated_smooth6') #'acpc_rotated_c+b.mask.bin'
cerebellum = NiftiImage(fid)
zeros = S.where(cerebellum.data[:,:,:] == 0)
zeroed = empty.copy()
zeroed.data[zeros] = 1

maskedmask = mask.data * zeroed.data
maskedmask = NiftiImage(maskedmask)
maskedmask.header = mask.header
maskedmask.save('mask.nii.gz')

