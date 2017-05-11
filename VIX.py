# -*- coding: utf-8 -*-
"""
Created on Tue Feb  7 15:31:04 2017

@author: Administrator
"""
from math import sqrt,exp

def calsigma(callPrice, putPrice, strike, T, r):
    # determine F
    diff = []
    lenlist = len(callPrice)
    for i in range(0, lenlist ):
        diff.append(abs(callPrice[i] - putPrice[i]))
    mindiff = min(diff)
    node0 = diff.index(min(diff))
    K0 = strike[node0]

    F = K0 + exp(r * T) * mindiff

    # determine K0
    minFK = F
    for i in range(0, lenlist ):
        
        if(strike[i] <= F and F - strike[i] < minFK):
            minFK = F - strike[i]
            K0node = i
    K0 = strike[K0node]
    
   
    # select both the put and call with strike price  K0
    deltaK = strike[1] - strike[0]
    QK = (callPrice[K0node] + putPrice[K0node])/2
    sumK = deltaK * exp(r * T) * QK / (K0 * K0)
    # select out-of-the-money put options with strike prices < K0
    for i in range(0, K0node):
        QK = putPrice[i]
        sumK += deltaK * exp(r * T) * QK / (strike[i] * strike[i])
    # select out-of-the-money call options with strike prices > K0
    for i in range(K0node + 1, lenlist):
        QK = callPrice[i]
        sumK += deltaK * exp(r * T) * QK / (strike[i] * strike[i])
    sigma = 2 * sumK / T - (F / K0 - 1) * (F / K0 - 1) / T
    return sigma
def calVIX(callPrice1, putPrice1, strike1, T1, callPrice2, putPrice2, strike2, T2, r):
    sigma1 = calsigma(callPrice1, putPrice1, strike1, T1, r)
    sigma2 = calsigma(callPrice2, putPrice2, strike2, T2, r)
    vxfc = 100 * sqrt(T1 * sigma1 * ((T2 * 525600 - 43200) /(T2 * 525600 - T1 * 525600)) + T2 * sigma2 * ((43200 - T1 * 525600) /(T2 * 525600 - T1 * 525600)) * 525600 / 43200)
    return vxfc
callPrice1=[0.1388,	0.09,	0.0453,	0.0155,	0.0037,	0.001]
putPrice1=[0.0008,	0.0013,	0.0059,	0.0263,	0.065,	0.115]
strike1 =[2.2,	2.25,	2.3,	2.35,	2.4,	2.45]
callPrice2=[0.1445,0.0994,0.0619,	0.0328,	0.016,	0.0074,	0.0033,	0.0029]
putPrice2 = [0.0032,0.0081,0.0199,	0.0411,	0.0748,	0.1156,	0.165,	0.215	]
strike2 =[2.2, 2.25, 2.3,	2.35,	2.4,	2.45,	2.5,	2.55]
T1 = 14/365
T2 = 42/365
r = 0.035
a = calVIX(callPrice1, putPrice1, strike1, T1, callPrice2, putPrice2, strike2, T2, r)
print(a)
           


