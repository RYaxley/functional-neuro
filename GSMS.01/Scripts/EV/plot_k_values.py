#!/usr/bin/env python
# encoding: utf-8
"""
plot_k_values.py

Created by Richard Yaxley on 2010-09-03.

"""

import sys
import os
import scipy as S
import pylab as P

k_values = S.linspace(0.001,.3,100)
# delays = [0,1,2,4,8]
delays = [0,7,14,28,56]
# delays = [0,30,60,90,120,150,180]
# delays = S.linspace(0,365,10)

LLR = 1.0

# Hyperbolic Discounting Function: SubjectiveValue = LLR/(1 + DiscountRate * Delay) 

for k in k_values:
    d = []
    for delay in delays:
        # Calculate the discounted value of the delayed amount
        value = LLR/(1 + k * delay)
        print k, delay, value
        d.append(value)
    P.plot(d)

        