# -*- coding: utf-8 -*-
#
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
def bs_call(spot, strike, r, d, vol, expiry):
	moneyness = log(spot / strike)
	stddev = vol * sqrt(expiry);
	d1 = (moneyness + (r - d) * expiry + 0.5 * stddev * stddev) / stddev
	d2 = d1 - stddev

	return spot * exp(-d * expiry) * stats.norm.cdf(d1, 0, 1) - strike * exp(-r * expiry) * stats.norm.cdf(d2, 0, 1)
 
def bs_put(spot, strike, r, d, vol, expiry):
	moneyness = log(spot / strike)
	stddev = vol * sqrt(expiry)
	d1 = (moneyness + (r - d) * expiry + 0.5 * stddev * stddev) / stddev
	d2 = d1 - stddev

	return strike * exp(-r * expiry) * stats.norm.cdf(-d2, 0, 1) - spot * exp(-d * expiry) * stats.norm.cdf(-d1, 0, 1)
 
def bs_call_delta( spot,  strike,  r,  d,  vol,  expiry): 
        moneyness = log(spot / strike)
        stddev = vol * sqrt(expiry)
        d1 = (moneyness + (r - d) * expiry + 0.5 * stddev * stddev) / stddev
	
        return exp(-d * expiry) * stats.norm.cdf(d1, 0, 1)
	
	
def bs_put_delta( spot,  strike,  r,  d,  vol,  expiry): 
        moneyness = log(spot / strike)
        stddev = vol * sqrt(expiry)
        d1 = (moneyness + (r - d) * expiry + 0.5 * stddev * stddev) / stddev
	
        return exp(-d * expiry) * (stats.norm.cdf(d1, 0, 1) - 1)
	
	
def bs_call_gamma( spot,  strike,  r,  d,  vol,  expiry): 
        moneyness = log(spot / strike)
        stddev = vol * sqrt(expiry)
        d1 = (moneyness + (r - d) * expiry + 0.5 * stddev * stddev) / stddev
	
        return exp(-d * expiry) * stats.norm.pdf(d1, 0, 1) / (spot * vol * sqrt(expiry))
	
	
def bs_put_gamma( spot,  strike,  r,  d,  vol,  expiry): 
        return bs_call_gamma(spot, strike, r, d, vol, expiry)
	
	
def bs_call_theta( spot,  strike,  r,  d,  vol,  expiry): 
        moneyness = log(spot / strike)
        stddev = vol * sqrt(expiry)
        d1 = (moneyness + (r - d) * expiry + 0.5 * stddev * stddev) / stddev
        d2 = d1 - stddev
        return d * spot * exp(-d * expiry) * stats.norm.cdf(d1, 0, 1) -spot * exp(-d * expiry) * vol * stats.norm.pdf(d1, 0, 1) / (2 * sqrt(expiry)) - r * strike * exp(-r * expiry) * stats.norm.cdf(d2, 0, 1)
	
	
def bs_put_theta( spot,  strike,  r,  d,  vol,  expiry): 
        moneyness = log(spot / strike)
        stddev = vol * sqrt(expiry)
        d1 = (moneyness + (r - d) * expiry + 0.5 * stddev * stddev) / stddev
        d2 = d1 - stddev
	
        return r * strike * exp(-r * expiry) * stats.norm.cdf(-d2, 0, 1) - d * spot * exp(-d * expiry) * stats.norm.cdf(-d1) - spot * exp(-d * expiry) * vol * stats.norm.pdf(d1, 0, 1) / (2 * sqrt(expiry))
	
	
def bs_call_vega( spot,  strike,  r,  d,  vol,  expiry): 
        moneyness = log(spot / strike)
        stddev = vol * sqrt(expiry)
        d1 = (moneyness + (r - d) * expiry + 0.5 * stddev * stddev) / stddev
	
        return spot * exp(-d * expiry) * sqrt(expiry) * stats.norm.pdf(d1, 0, 1)
	
	
def bs_put_vega( spot,  strike,  r,  d,  vol,  expiry): 
        return bs_call_vega(spot, strike, r, d, vol, expiry)
	
	
def bs_call_rho( spot,  strike,  r,  d,  vol,  expiry): 
        moneyness = log(spot / strike)
        stddev = vol * sqrt(expiry)
        d1 = (moneyness + (r - d) * expiry + 0.5 * stddev * stddev) / stddev
        d2 = d1 - stddev
	
        return strike * expiry * exp(-r * expiry) * stats.norm.cdf(d2)
	
	
def bs_put_rho( spot,  strike,  r,  d,  vol,  expiry): 
        moneyness = log(spot / strike)
        stddev = vol * sqrt(expiry)
        d1 = (moneyness + (r - d) * expiry + 0.5 * stddev * stddev) / stddev
        d2 = d1 - stddev
	
        return -strike * expiry * exp(-r * expiry) * stats.norm.cdf(-d2)
	


