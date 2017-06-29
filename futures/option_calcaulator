# -*- coding: utf-8 -*-
"""
Created on Mon Jun  5 15:14:21 2017

@author: Administrator
"""

from math import log,sqrt,exp
from scipy.stats import norm
def option_pricer(spot,strike,maturity,r,vol):
    d1=(log(spot/strike)+(r+0.5*vol*vol)*maturity)/vol/sqrt(maturity)
    d2=d1-vol*sqrt(maturity)
    call=spot*norm.cdf(d1)-strike*exp(-r*maturity)*norm.cdf(d2)
    put=call+strike-spot
    return (call,put)

call,put=option_pricer(spot=200,strike=180,maturity=0.164383562
,r=0,vol=0.29)

#print('期权call价格:%.6f'%call)

#print('期权put价格:%.6f'%put)



print('call price is :',call)
print('put price is :',put)
    
