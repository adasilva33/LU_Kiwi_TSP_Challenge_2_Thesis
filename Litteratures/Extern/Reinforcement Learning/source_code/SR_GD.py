# -*- coding: utf-8 -*-
"""
Created on Sat Jul 27 13:30:02 2019

@author: pylya
"""

import Calculations
import Operators
import time
import numpy as np

def HH(sol, areas_and_airports, mydict, areas_n, start_time, run_time):
    cost = Calculations.CalculateCost(sol,mydict,areas_n)
    cost_best = cost
    solBest_0 = sol[0].copy()
    solBest_1 = sol[1].copy()
    LLH0 = lambda: Operators.Swap2(sol[0],sol[1],x,y)
    LLH1 = lambda: Operators.Insert(sol[0],sol[1],x,y)
    LLH2 = lambda: Operators.Reverse(sol[0],sol[1],r,rr)
    LLH3 = lambda: Operators.Change_Airport(sol[1],sol[0],x,yy,areas_and_airports)
    LLHS = [LLH0,LLH1,LLH2,LLH3]
    f = 97859
    delta = cost - f
    while time.time() - start_time < run_time:
        time_now = time.time() - start_time
        Rev = False
        CAL = False
        copy_0 = sol[0].copy()
        copy_1 = sol[1].copy()
        x = np.random.randint(1,areas_n)
        y = np.random.randint(1,areas_n)
        yy = np.random.randint(1,areas_n+1)
        r = np.random.randint(1,areas_n-2)
        rr = np.random.randint(r+2,areas_n)
        l = np.random.randint(0,len(LLHS))
        c = float(np.random.random(1))
        if l == 3 and yy == areas_n:
            CAL = True
            y = areas_n
        if l == 1 or l == 2:
            Rev = True
            x = r
            y = rr
        else:
            Rev = False
        LLHS[l]()
        if l != 3 and c >= 0.5:
            LLH3()
        f_after = Calculations.PFeas(sol,mydict,areas_n,x,y,Rev,CAL)
        if f_after == 0:
            cost_new = Calculations.CalculateCost(sol,mydict,areas_n)
            t = f + delta * (1 - (time_now / run_time))
            if cost_new <= t:
                if cost_new <= cost_best:
                    cost_best = cost_new
                    solBest_0 = sol[0].copy()
                    solBest_1 = sol[1].copy()
            else:
                sol[0] = copy_0
                sol[1] = copy_1
        else:
            sol[0] = copy_0
            sol[1] = copy_1
    sol[0] = solBest_0
    sol[1] = solBest_1