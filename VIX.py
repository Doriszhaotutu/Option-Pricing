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
        diff.append(callPrice[i] - putPrice[i])
    mindiff = min(diff)
    node0 = diff.index(min(diff))
    K0 = strike[node0]

    F = K0 + exp(r * T) * mindiff
    # determine K0
    for i in range(0, lenlist ):
        minFK = F
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
           


