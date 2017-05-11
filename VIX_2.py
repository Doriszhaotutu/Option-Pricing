# -*- coding: utf-8 -*-
"""
Created on Thu Feb  9 14:34:19 2017

@author: Administrator
"""

from math import sqrt,exp

def calsigma(callAsk, callBid, putAsk, putBid, strike, T, r):
    # determine F
    diff = []
    lenlist = len(strike)
    callPrice = []
    putPrice = []
    for i in range(0, lenlist ):
        callPrice.append(0.5 * (callAsk[i] + callBid[i]))
        putPrice.append(0.5 * (putAsk[i] + putBid[i]))
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
    strikein = strike[K0node]    
    for i in range(K0node - 1, -1, -1):
        if(putBid[i] == 0 and putBid[i + 1] == 0 ):
            break
        if(putBid[i] > 0):
            if(i == 0):
                if(putBid[1] > 0):
                    deltaK = strike[1] - strike[0]
                else:
                    deltaK = strike[2] - strike[0]
            else:
                if(putBid[i - 1] > 0):                    
                    deltaK = (strikein - strike[i - 1])/2
                else:
                    deltaK = (strikein - strike[i - 2])/2
            QK = putPrice[i]
            print( deltaK)
            sumK += deltaK * exp(r * T) * QK / (strike[i] * strike[i])
            strikein = strike[i]
    # select out-of-the-money call options with strike prices > K0
    strikein = strike[K0node]
    for i in range(K0node + 1, lenlist):
        if(callBid[i] == 0 and callBid[i - 1] == 0 ):
            break
        if(callBid[i] > 0):
            if(i == lenlist -1):
                if(callBid[lenlist - 2] > 0):
                    deltaK = strike[lenlist - 1] - strike[lenlist - 2]
                else:
                    deltaK = strike[lenlist - 1] - strike[lenlist - 3]
            else:
                if(callBid[i + 1] > 0):
                    deltaK = (strike[i + 1] - strikein)/2
                else:
                    deltaK = (strike[i + 2] - strikein)/2
            QK = callPrice[i]
            #print( deltaK)
            sumK += deltaK * exp(r * T) * QK / (strike[i] * strike[i])
            strikein = strike[i]
    sigma = 2 * sumK / T - (F / K0 - 1) * (F / K0 - 1) / T
    return sigma
def calVIX(callAsk1, callBid1, putAsk1, putBid1, strike1, T1, callAsk2, callBid2, putAsk2, putBid2, strike2, T2, r):
    sigma1 = calsigma(callAsk1, callBid1, putAsk1, putBid1, strike1, T1, r)
    sigma2 = calsigma(callAsk2, callBid2, putAsk2, putBid2, strike2, T2, r)
    vxfc = 100 * sqrt(T1 * sigma1 * ((T2 * 525600 - 43200) /(T2 * 525600 - T1 * 525600)) + T2 * sigma2 * ((43200 - T1 * 525600) /(T2 * 525600 - T1 * 525600)) * 525600 / 43200)
    return vxfc

callAsk1 = [0.1529,	0.1037,	0.0567,	0.0206,	0.0053,	0.0011]
callBid1 = [0.1527,	0.1035,	0.0565,	0.0203,	0.0052,	0.001]
strike1 = [2.2,	2.25,	2.3,	2.35,	2.4,	2.45]
putBid1 = [0.0005,	0,	0.004,	0.0178,	0.0524,	0.0982]
putAsk1 = [0.0006,	0.0009,	0.0041,	0.0179,	0.0526,	0.0906]
callAsk2 = [0.1573,	0.1112,	0.0706,	0.0391,	0.0202,	0.0091,	0.0039,	0.0027]
callBid2 = [0.157,	0.1107,	0.0704,	0.039,	0.0201,	0.009,	0.0038,	0.0025]
strike2 = [2.2,	2.25,	2.3,	2.35,	2.4,	2.45,	2.5,	2.55]
putBid2 = [0.0025,	0.0063,	0.0157,	0.0345,	0.065,	0.1042,	0.1492,	0.1966]
putAsk2 = [0.0026,	0.0065,	0.0159,	0.0347,	0.0654,	0.1045,	0.0196,	0.1969]
T1 = 13/365
T2 = 41/365
r = 0.035
b= calVIX(callAsk1, callBid1, putAsk1, putBid1, strike1, T1, callAsk2, callBid2, putAsk2, putBid2, strike2, T2, r)
print(b)