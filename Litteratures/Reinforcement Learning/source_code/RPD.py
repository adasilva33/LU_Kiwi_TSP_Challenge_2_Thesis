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
    LLH0 = lambda: Operators.Swap2(sol[0],sol[1],x,y)
    LLH1 = lambda: Operators.Insert(sol[0],sol[1],x,y)
    LLH2 = lambda: Operators.Reverse(sol[0],sol[1],r,rr)
    LLH3 = lambda: Operators.Change_Airport(sol[1],sol[0],x,yy,areas_and_airports)
    LLHS = [LLH0,LLH1,LLH2,LLH3]
    perm = np.random.randint(0,4,size=1000000)
    iteration = -1
    while time.time() - start_time < run_time:
        Rev = False
        CAL = False
        iteration += 1
        copy_0 = sol[0].copy()
        copy_1 = sol[1].copy()
        x = np.random.randint(1,areas_n)
        y = np.random.randint(1,areas_n)
        yy = np.random.randint(1,areas_n+1)
        r = np.random.randint(1,areas_n-2)
        rr = np.random.randint(r+2,areas_n)
        c = float(np.random.random(1))
        if perm[iteration] == 3 and yy == areas_n:
            CAL = True
            y = areas_n
        if perm[iteration] == 1 or perm[iteration] == 2:
            Rev = True
            x = r
            y = rr
        else:
            Rev = False
        LLHS[perm[iteration]]()
        if LLHS[perm[iteration]] != LLH3 and c >= 0.5:
            LLH3()
        f_after = Calculations.PFeas(sol,mydict,areas_n,x,y,Rev,CAL)
        if f_after == 0:
            cost_new = Calculations.CalculateCost(sol,mydict,areas_n)
            while (cost_new < cost and f_after == 0) and time.time() - start_time + 0.5 < run_time:
                cost = cost_new
                copy_0 = sol[0].copy()
                copy_1 = sol[1].copy()
                x = np.random.randint(1,areas_n)
                y = np.random.randint(1,areas_n)
                yy = np.random.randint(1,areas_n+1)
                r = np.random.randint(1,areas_n-2)
                rr = np.random.randint(r+2,areas_n)
                c = float(np.random.random(1))
                if perm[iteration] == 3 and yy == areas_n:
                    CAL = True
                    y = areas_n
                if perm[iteration] != 2:
                    Rev = False
                else:
                    Rev = True
                LLHS[perm[iteration]]()
                if LLHS[perm[iteration]] != LLH3 and c >= 0.5:
                    LLH3()
                f_after = Calculations.PFeas(sol,mydict,areas_n,x,y,Rev,CAL)
                cost_new = Calculations.CalculateCost(sol,mydict,areas_n)
            else:
                sol[0] = copy_0
                sol[1] = copy_1
        else:
            sol[0] = copy_0
            sol[1] = copy_1