# -*- coding: utf-8 -*-
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


def brent(a, b,  price, func, func2, func3, spot, strike, r,  d,  expiry, ssteps,tsteps):
    dd = None    
    niters = 0
    if(func):
          fa = func(spot, strike, r, d, a, expiry)
    else:
          if(func2):
              fa = func2(spot, strike, r, d, a, expiry, tsteps)
          else:
              fa = func3(spot, strike, r, d, a, expiry, ssteps, tsteps)
    if(func):
          fb = func(spot, strike, r, d, b, expiry)
    else:
          if(func2):
              fb = func2(spot, strike, r, d, b, expiry, tsteps)
          else:
              fb = func3(spot, strike, r, d, b, expiry, ssteps, tsteps)        
              
	
	#root is not bracketed 
    if ((fa - price) * (fb - price) >= 0.0):
        
        return "NAN1 fa fb same direction"
	#swap 
    if (abs(fa) < abs(fb)):#>OR<?
         t = a 
         ft = fa
         a  = b
         b  = t
         fa = fb
         fb = ft
	
    c = a
    fc = fa
    mflag = 1
    while (niters < 500): 
		#convergence
        if (abs(fb - price) <= 0.000001 or abs(b - a) <= 0.0001):
            return b
        if (abs(fa - fc) > 0.000001 and abs(fb - fc) > 0.000001):
			# inverse quadratic interpolation 
            s = a * fb * fc / ((fa - fb) * (fa - fc)) + b * fa * fc / ((fb - fa) * (fb - fc)) + c * fa * fb / ((fc - fa) * (fc - fb))
        else:
			#secant method 
            s = b - fb * (b - a) / (fb - fa)
       
        if ((s < 0.25 * (3.0 * a + b) or s > b) or( mflag and abs(s - b) >= 0.5 * abs(b - c)) or(not mflag and abs(s - b) >= 0.5 * abs(c - dd)) or( mflag and abs(b - c) < 0.0001) or(not mflag and abs(c - dd) < 0.0001)):
			#bisection method
            s = 0.5 * (a + b)
            mflag = 1
        else:
            mflag = 0
        if(func):
            fs = func(spot, strike, r, d, s, expiry)
        else:
            if(func2):
                fs = func2(spot, strike, r, d, s, expiry, tsteps)
            else:
                fs = func3(spot, strike, r, d, s, expiry, ssteps, tsteps)
        dd = c
        c = b 
        fc = fb
        if ((fa - price) * (fs - price) < 0.0) :
            b  = s
            fb = fs
        else:
            a  = s
            fa = fs
		
		# swap 
        if (abs(fa) < abs(fb)):
            t = a
            ft = fa
            a  = b
            b  = t
            fa = fb
            fb = ft
		
        niters += 1	
    return "NAN500"

