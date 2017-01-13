# -*- coding: utf-8 -*-
#!/usr/bin/python
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
from brent import *

# FIXME
#计算期货期权时，需要设置d的值与利率相等 
def bi_amer_call( spot,  strike,  r,  d,  vol,  expiry,  steps):
    dt = expiry / steps
    # erest rate for each step 
    R = exp(r* dt)
    # inverse of erest rate 
    Rinv = 1.0 / R
    # up movement 
    up = exp(vol * sqrt(dt))
    uu = up * up
    # down movement 
    dn = 1.0 / up
    p_up = (exp((r - d )* dt) - dn) / (up - dn)
    p_dn = 1.0 - p_up
    prices = [0] * (steps + 1)
    call_values = [0] * (steps + 1)
    prices[0] = spot * pow(dn, steps)
    call_values[0] = max(0.0, prices[0] - strike)
    for i in range(1, steps + 1 ):
        # price of underlying 
        prices[i] = uu * prices[i - 1]#计算出树的终结点
        # value of corresponding call 
    for i in range(0, steps + 1):
        call_values[i] = max(0.0, prices[i] - strike) 
    for j in range(steps - 1, -1, -1):
        for i in range(0, j + 1): 
            call_values[i] = Rinv * (p_up * call_values[i + 1] + p_dn * call_values[i])
            prices[i] = dn * prices[i + 1]
            call_values[i] = max(call_values[i], prices[i] - strike)
           # print(call_values[i])
    res = call_values[0]
    return res
	
	
# FIXME 
def bi_amer_put( spot,  strike,  r,  d,  vol,  expiry,  steps):   
    dt = expiry / steps
    # erest rate for each step 
    R = exp(r   * dt)
    # inverse of erest rate 
    Rinv = 1.0 / R 
    # up movement 
    up = exp(vol * sqrt(dt))    
    uu = up * up
    # down movement 
    dn = 1.0 / up    
    p_up = (exp((r - d)  * dt) - dn) / (up - dn)
    p_dn = 1.0 - p_up
    prices = [0] * (steps + 1)
    put_values = [0] * (steps + 1)
    prices[0] = spot * pow(dn, steps)   
    
    for i in range(1, steps + 1 ):
        # price of underlying 
        prices[i] = uu * prices[i - 1]#计算出树的终结点
        # value of corresponding put
    for i in range(0, steps + 1):
        put_values[i] = max(0.0, strike - prices[i])   
        
    for j in range(steps - 1, -1, -1):
        for i in range(0, j + 1): 
            put_values[i] = Rinv * (p_up * put_values[i + 1] + p_dn * put_values[i])           
            prices[i] = dn * prices[i + 1]           
            put_values[i] = max(put_values[i], strike - prices[i ])
           
        
    res = put_values[0]        
    return res
	
 
 
 # FIXME 
def  bi_amer_call_greeks( spot,  strike,  r,  d,  vol,  expiry,  steps):
    dt = expiry / steps
    # erest rate for each step 
    R = exp(r * dt)
    # inverse of erest rate 
    Rinv = 1.0 / R
    # up movement 
    up = exp(vol * sqrt(dt))
    uu = up * up
    # down movement 
    dn = 1.0 / up
    p_up = (exp((r - d) * dt) - dn) / (up - dn)
    p_dn = 1.0 - p_up
    prices = [0] * (steps + 1)
    call_values = [0] * (steps + 1)
    prices[0] = spot * pow(dn, steps)
    call_values[0] = max(0.0, prices[0] - strike)
    for i in range(1, steps + 1 ):
        # price of underlying 
        prices[i] = uu * prices[i - 1]
        # value of corresponding call 
        call_values[i] = max(0.0, prices[i] - strike)
    for j in range(steps - 1, 1, -1):
        for i in range(0, j + 1): 	
            call_values[i] = Rinv * (p_up * call_values[i + 1] + p_dn * call_values[i])
            prices[i] = dn * prices[i + 1]
            call_values[i] = max(call_values[i], prices[i] - strike)
    f22 = call_values[2]
    f21 = call_values[1]
    f20 = call_values[0]
    for i in range(2):
        call_values[i] = Rinv * (p_up * call_values[i + 1] + p_dn * call_values[i])
        prices[i] = dn * prices[i + 1]
        call_values[i] = max(call_values[i], prices[i] - strike)
    f11 = call_values[1]
    f10 = call_values[0]
    call_values[0] = Rinv * (p_up * call_values[1] + p_dn * call_values[0])
    prices[0] = dn * prices[1]
    call_values[0] = max(call_values[0], prices[0] - strike)
    f00 = call_values[0]
    delta = (f11 - f10) / (spot * up - spot * dn)
    gamma = ((f22 - f21) / (spot * uu - spot) - (f21 - f20) / (spot - spot * dn * dn)) / (0.5 * (spot * uu - spot * dn * dn))
    theta = (f21 - f00) / (2 * dt)
    vega  = (bi_amer_call(spot, strike, r, d, vol + 0.02, expiry, steps) - f00) / 0.02
    rho   = (bi_amer_call(spot, strike, r *1.01, d *1.01, vol, expiry, steps) - f00) / (r * 0.01)
    return delta, gamma, theta, vega, rho
'''
#下面这种方法也可算出Greeks，但是我认为这种方法有较多的重复的代码。不够好。	
# FIXME 
def bi_amer_put_greeks( spot,  strike,  r,  d,  vol,  expiry,  steps):
    dt = expiry / steps
    # erest rate for each step 
    R = exp(r * dt)
    # inverse of erest rate 
    Rinv = 1.0 / R
    # up movement 
    up = exp(vol * sqrt(dt))
    uu = up * up
    # down movement 
    dn = 1.0 / up
    p_up = (exp((r - d) * dt) - dn) / (up - dn)
    p_dn = 1.0 - p_up
    prices = [0] * (steps + 1)
    put_values = [0] * (steps + 1)
    prices[0] = spot * pow(dn, steps)
    prices[0] = spot * pow(dn, steps)
    put_values[0] = max(0.0, strike - prices[0])
    for i in range(1, steps + 1 ):
        # price of underlying 
        prices[i] = uu * prices[i - 1]
        # value of corresponding put 
        put_values[i] = max(0.0, strike - prices[i])
    for j in range(steps - 1, 1, -1):
        for i in range(0, j + 1):
            put_values[i] = Rinv * (p_up * put_values[i + 1] + p_dn * put_values[i])
            prices[i] = dn * prices[i + 1]
            put_values[i] = max(put_values[i], strike - prices[i])
    f22 = put_values[2]
    f21 = put_values[1]
    f20 = put_values[0]
    for i in range(2):	
        put_values[i] = Rinv * (p_up * put_values[i + 1] + p_dn * put_values[i])
        prices[i] = dn * prices[i + 1]
        put_values[i] = max(put_values[i], strike - prices[i])
    f11 = put_values[1]
    f10 = put_values[0]
    put_values[0] = Rinv * (p_up * put_values[1] + p_dn * put_values[0])
    prices[0] = dn * prices[1]
    put_values[0] = max(put_values[0], strike - prices[0])
    f00 = put_values[0]
    delta = (f11 - f10) / (spot * up - spot * dn)
    gamma = ((f22 - f21) / (spot * uu - spot) - (f21 - f20) / (spot - spot * dn * dn)) /(0.5 * (spot * uu - spot * dn * dn))
    theta = (f21 - f00) / (2 * dt)
    vega  = (bi_amer_put(spot, strike, r, d, vol + 0.02, expiry, steps) - f00) / 0.02
    rho   = (bi_amer_put(spot, strike, r * 1.01, d * 1.01, vol, expiry, steps) - f00) / (r * 0.01)
    return delta, gamma, theta, vega, rho
'''
def bi_call_delta( spot,  strike,  r,  b,  vol,  expiry,  steps): 
    return (bi_amer_call(1.001 * spot, strike, r, b, vol, expiry,  steps) - bi_amer_call(0.999 * spot, strike, r, b, vol, expiry,  steps)) / (0.002 * spot)

def bi_put_delta( spot,  strike,  r,  b,  vol,  expiry,  steps): 
    return (bi_amer_put(1.001 * spot, strike, r, b, vol, expiry,  steps) - bi_amer_put(0.999 * spot, strike, r, b, vol, expiry,  steps)) / (0.002 * spot)	

	# FIXME 
def bi_call_gamma( spot,  strike,  r,  b,  vol,  expiry, steps): 
    return (bi_call_delta(1.01 * spot, strike, r, b, vol, expiry, steps) - bi_call_delta(0.99 * spot, strike, r, b, vol, expiry, steps)) / (0.02 * spot)
	
	
	# FIXME 
def bi_put_gamma( spot,  strike,  r,  b,  vol,  expiry, steps): 
    return (bi_put_delta(1.01 * spot, strike, r, b, vol, expiry, steps) - bi_put_delta(0.99 * spot, strike, r, b, vol, expiry, steps)) / (0.02 * spot)
	
	
	# FIXME 
def bi_call_theta( spot,  strike,  r,  b,  vol,  expiry, steps): 
    return (bi_amer_call(spot, strike, r, b, vol, 1.01 * expiry, steps) - bi_amer_call(spot, strike, r, b, vol, 0.99 * expiry, steps)) / (- 0.02 * expiry)
	
	
	# FIXME 
def bi_put_theta( spot,  strike,  r,  b,  vol,  expiry, steps): 
    return (bi_amer_put(spot, strike, r, b, vol, 1.01 * expiry, steps) - bi_amer_put(spot, strike, r, b, vol, 0.99 * expiry, steps)) / ( - 0.02 * expiry)
	
	
	# FIXME 
def bi_call_vega( spot,  strike,  r,  b,  vol,  expiry, steps): 
    return (bi_amer_call(spot, strike, r, b, 1.001 * vol, expiry, steps) - bi_amer_call(spot, strike, r, b, 0.999 * vol, expiry, steps)) / (0.002 * vol)
	
	
	# FIXME 
def bi_put_vega( spot,  strike,  r,  b,  vol,  expiry, steps): 
    return (bi_amer_put(spot, strike, r, b, 1.001 * vol, expiry, steps) - bi_amer_put(spot, strike, r, b, 0.999 * vol, expiry, steps)) / (0.002 * vol)
	
	
	# FIXME 
def bi_call_rho( spot,  strike,  r,  b,  vol,  expiry, steps): 
    return (bi_amer_call(spot, strike, 1.01 * r, b, vol, expiry, steps) - bi_amer_call(spot, strike, 0.99 * r, b, vol, expiry, steps)) / (0.02 * r)
	
	
	# FIXME 
def bi_put_rho( spot,  strike,  r,  b,  vol,  expiry, steps): 
    return (bi_amer_put(spot, strike, 1.01 * r, b, vol, expiry, steps) -bi_amer_put(spot, strike, 0.99 * r, b, vol, expiry, steps)) / (0.02 * r)
    
    
	# FIXME 
def impv_bi( spot,  strike,  r,  d,  expiry, steps, price,  optiontype):
    low = 0.001
    high = 0.3
    if (optiontype != "AMER_CALL" and optiontype != "AMER_PUT"):
        return "optiontype error"
    if(optiontype == "AMER_CALL"):
        ce = bi_amer_call(spot, strike, r, d, high, expiry, steps)
    else:
        ce = bi_amer_put(spot, strike, r, d, high, expiry, steps)

    while (ce < price): 
        high *= 2.0
        if (high > 1e10):
            return "can't find a high vol"
        if(optiontype == "AMER_CALL"):
            ce = bi_amer_call(spot, strike, r, d, high, expiry, steps)
        else:
            ce = bi_amer_put(spot, strike, r, d, high, expiry, steps)
	
    if(optiontype == "AMER_CALL"):	
        return brent(low, high, price, None, bi_amer_call, None, spot, strike, r, d, expiry, 0, steps)
    else:
        return brent(low, high, price, None,  bi_amer_put, None, spot, strike, r, d, expiry, 0, steps)	


	

