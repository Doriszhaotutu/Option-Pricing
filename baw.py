# -*- coding: utf-8 -*-
# usr/bin/bash -tt
# Copyright (c) 2016 by Yuchao Zhao, Xiaoye Meng.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
from math import log,sqrt,exp
from scipy import stats
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from bs import *
#计算期货期权时，b的值需要设置为0
def baw_call( spot,  strike,  r,  b,  vol,  expiry): 
     M = 2.0 * r / (vol * vol)
     N = 2.0 *  b / (vol * vol)
     K = 1.0 - exp(-r * expiry)
     q2 = 0.5 * (-(N - 1) + sqrt((N - 1) * (N - 1) + 4 * M / K))
     q2inf = 0.5 *(-(N - 1) + sqrt((N - 1) * (N - 1) + 4 * M))        
     Ssinf = strike / (1.0 - 1.0 / q2inf)
     stddev = vol * sqrt(expiry)
     h2 = -( b * expiry + 2.0 * stddev) * (strike / (Ssinf - strike))
     S0 = strike + (Ssinf - strike) * (1.0 - exp(h2))
     g = 1.0
     gprime = 1.0
     niters = 0
     Si = S0

     while(abs(g) > 0.000001 and abs(gprime) > 0.000001 and niters < 500 and Si > 0.0): 
        ce = bs_call(Si, strike, r, r - b, vol, expiry)
        d1 = (log(Si / strike) + b * expiry + 0.5 * stddev * stddev) / stddev
        g = (1.0 - 1.0 / q2) * Si - strike - ce + (1.0 / q2) * Si * exp(-( r - b ) * expiry) * stats.norm.cdf(d1, 0, 1)
        gprime = (1.0 - 1.0 / q2) * (1.0 - exp(-(r - b) * expiry)) * stats.norm.cdf(d1, 0, 1) + (1.0 / q2) * exp(-(r - b ) * expiry) * stats.norm.cdf(d1, 0, 1) * (1.0 / stddev)
        Si -= g/gprime
        niters += 1
    
     if(abs(g) > 0.000001):
        Ss = S0
     else:
        Ss = Si
     ce = bs_call(spot, strike, r, r - b, vol, expiry)
     if (spot >= Ss):
        ca = spot - strike
     else: 
        d1 = (log(Ss / strike) +  b * expiry + 0.5 * stddev * stddev) / stddev
        A2 = (Ss / q2) * (1.0 - exp(-(r - b) * expiry) * stats.norm.cdf(d1, 0, 1))
        ca = ce + A2 * pow(spot / Ss, q2)
		
     return max(ca,ce)
	
	
	# FIXME 
def baw_put( spot,  strike,  r,  b,  vol,  expiry): 
    M = 2.0 * r / (vol * vol)
    N = 2.0 *  b / (vol * vol)
    K = 1.0 - exp(-r * expiry)
    q1 = 0.5 * (-(N - 1) - sqrt((N - 1) * (N - 1) + 4 * M / K))
    q1inf = 0.5 *(-(N - 1) - sqrt((N - 1) * (N - 1) + 4 * M))
    Ssinf = strike / (1.0 - 1.0 / q1inf)
    stddev = vol * sqrt(expiry)
    h1 = ( b * expiry - 2.0 * stddev) * (strike / (strike - Ssinf))
    S0 = Ssinf + (strike - Ssinf) * exp(h1)
    g = 1.0
    gprime = 1.0
    niters = 0
    Si = S0
    while (abs(g) > 0.000001 and abs(gprime) > 0.000001 and niters < 500 and Si > 0.0):
         pe = bs_put(Si, strike, r, r - b, vol, expiry)
         d1 = (log(Si / strike) +  b * expiry + 0.5 * stddev * stddev) / stddev
         g = strike - Si - pe + (1.0 / q1) * Si * (1.0 - exp(-(r-b) * expiry)) * stats.norm.cdf(-d1, 0, 1)
         gprime = (1.0 / q1 - 1.0) * (1.0 - exp(-(r-b) * expiry)) * stats.norm.cdf(-d1, 0, 1) + (1.0 / q1) * exp(-(r-b) * expiry) * stats.norm.cdf(-d1, 0, 1) * (1.0 / stddev)
         Si -= g/gprime
         niters += 1
    if(abs(g) > 0.000001):
        Ss = S0
    else:
        Ss = Si
    pe = bs_put(spot, strike, r, r - b, vol, expiry)
    if (spot <= Ss):
        pa = strike - spot
    else: 
        d1 = (log(Ss / strike) +  b * expiry + 0.5 * stddev * stddev) / stddev
        A1 = (-Ss / q1) * (1.0 - exp(-(r-b) * expiry) * stats.norm.cdf(-d1, 0, 1))
        pa = pe + A1 * pow(spot / Ss, q1)
    return max(pa,pe)
	
	
	# FIXME 
def baw_call_delta( spot,  strike,  r,  b,  vol,  expiry): 
    return (baw_call(1.001 * spot, strike, r, b, vol, expiry) - baw_call(0.999 * spot, strike, r, b, vol, expiry)) / (0.002 * spot)
	
	
	# FIXME 
def baw_put_delta( spot,  strike,  r,  b,  vol,  expiry): 
    return (baw_put(1.001 * spot, strike, r, b, vol, expiry) - baw_put(0.999 * spot, strike, r, b, vol, expiry)) / (0.002 * spot)
	
	
	# FIXME 
def baw_call_gamma( spot,  strike,  r,  b,  vol,  expiry): 
    return (baw_call_delta(1.01 * spot, strike, r, b, vol, expiry) - baw_call_delta(0.99 * spot, strike, r, b, vol, expiry)) / (0.02 * spot)
	
	
	# FIXME 
def baw_put_gamma( spot,  strike,  r,  b,  vol,  expiry): 
    return (baw_put_delta(1.01 * spot, strike, r, b, vol, expiry) - baw_put_delta(0.99 * spot, strike, r, b, vol, expiry)) / (0.02 * spot)
	
	
	# FIXME 
def baw_call_theta( spot,  strike,  r,  b,  vol,  expiry): 
    return (baw_call(spot, strike, r, b, vol, 1.01 * expiry) - baw_call(spot, strike, r, b, vol, 0.99 * expiry)) / ( - 0.02 * expiry)
	
	
	# FIXME 
def baw_put_theta( spot,  strike,  r,  b,  vol,  expiry): 
    return (baw_put(spot, strike, r, b, vol, 1.01 * expiry) - baw_put(spot, strike, r, b, vol, 0.99 * expiry)) / (- 0.02 * expiry)
	
	
	# FIXME 
def baw_call_vega( spot,  strike,  r,  b,  vol,  expiry): 
    return (baw_call(spot, strike, r, b, 1.001 * vol, expiry) - baw_call(spot, strike, r, b, 0.999 * vol, expiry)) / (0.002 * vol)
	
	
	# FIXME 
def baw_put_vega( spot,  strike,  r,  b,  vol,  expiry): 
    return (baw_put(spot, strike, r, b, 1.001 * vol, expiry) - baw_put(spot, strike, r, b, 0.999 * vol, expiry)) / (0.002 * vol)
	
	
	# FIXME 
def baw_call_rho( spot,  strike,  r,  b,  vol,  expiry): 
    return (baw_call(spot, strike, 1.01 * r, b, vol, expiry) - baw_call(spot, strike, 0.99 * r, b, vol, expiry)) / (0.02 * r)
	
	
	# FIXME 
def baw_put_rho( spot,  strike,  r,  b,  vol,  expiry): 
    return (baw_put(spot, strike, 1.01 * r, b, vol, expiry) -baw_put(spot, strike, 0.99 * r, b, vol, expiry)) / (0.02 * r)
	
	
	# FIXME 
def impv_baw( spot,  strike,  r,  b,  expiry,  price, optiontype): 
    low = 0.000001
    high = 0.3
	
		# FIXME 
    if (optiontype != "AMER_CALL" and optiontype != "AMER_PUT"):
        return "NAN1"   
    if(optiontype == "AMER_CALL"):
        ce = baw_call(spot, strike, r, b, high, expiry)
    else:
        ce = baw_put(spot, strike, r, b, high, expiry)
    while (ce < price): 
        high *= 2.0
        if (high > 1e10):
            return "NAN2"
        if(optiontype == "AMER_CALL"):
            ce = baw_call(spot, strike, r, b, high, expiry)
        else:
            ce = baw_put(spot, strike, r, b, high, expiry)

    if(optiontype == "AMER_CALL"):	
        return brent(low, high, price, baw_call, None, None, spot, strike, r, b, expiry, 0, 0)
    else:
        return brent(low, high, price, baw_put,  None, None, spot, strike, r, b, expiry, 0, 0)
        


