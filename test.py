# -*- coding: utf-8 -*-
"""
Created on Wed Jan 11 11:19:03 2017

@author: Administrator
"""
from VIX import *
callPrice1=[0.1388,	0.09,	0.0453,	0.0155,	0.0037,	0.001]
putPrice1=[0.0008,	0.0013,	0.0059,	0.0263,	0.065,	0.115]
strike1 =[2.2,	2.25,	2.3,	2.35,	2.4,	2.45]
callPrice2=[0.0619,	0.0328,	0.016,	0.0074,	0.0033,	0.0029,	0.0994,	0.1445]
putPrice2 = [0.0199,	0.0411,	0.0748,	0.1156,	0.165,	0.215,	0.0081,	0.0032]
strike2 =[2.3,	2.35,	2.4,	2.45,	2.5,	2.55,	2.25,	2.2]
T1 = 14/252
T2 = 42/252
r = 0.035
a = calVIX(callPrice1, putPrice1, strike1, T1, callPrice2, putPrice2, strike2, T2, r)
