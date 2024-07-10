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
    LLH2 = lambda: Operators.Change_Airport(sol[1],sol[0],x,yy,areas_and_airports)
    LLH3 = lambda: Operators.Reverse(sol[0],sol[1],x,y)
    LLHS = [LLH0,LLH1,LLH2,LLH3]
    scores = [0.5,0.5,0.5,0.5]
    b = 0
    cost_best = cost
    solBest_0 = sol[0].copy()
    solBest_1 = sol[1].copy()
    iteration = -1
    a = 1000
    while time.time() - start_time < run_time:
        iteration += 1
        d = False
        CAL = False
        Rev = False
        copy_0 = sol[0].copy()
        copy_1 = sol[1].copy()
        x = np.random.randint(1,areas_n)
        y = np.random.randint(1,areas_n)
        yy = np.random.randint(1,areas_n+1)
        best = max(scores)
        index = scores.index(best)
        if index == 2 and yy == areas_n:
            CAL = True
        if index == 2:
            y = yy
        if index == 1 or index == 3:
            Rev = True
        cost_before = Calculations.PCost(sol,mydict,areas_n,x,y,Rev,CAL)
        LLHS[index]()
        f_after = Calculations.PFeas(sol,mydict,areas_n,x,y,Rev,CAL)
        if b > a:
            d = True
        if f_after == 0:
            cost_after = Calculations.PCost(sol,mydict,areas_n,x,y,Rev,CAL)
            if cost_after < cost_before or (b > a and cost_after < cost_before*1.3): 
                cost_new = Calculations.CalculateCost(sol,mydict,areas_n)
                if cost_new < cost_best:
                    cost_best = cost_new
                    solBest_0 = sol[0].copy()
                    solBest_1 = sol[1].copy()
                scores[index] += 0.1 * iteration*2*0.015
                b = 0
            else:
                sol[0] = copy_0
                sol[1] = copy_1
                scores[index] -= 0.1 * iteration/2*0.01
                b += 1
        else:
            sol[0] = copy_0
            sol[1] = copy_1
            scores[index] -= 0.1 * iteration/2*0.0125
            b += 10
        if d == True:
            scores = [0.5,0.5,0.5,0.5]
    sol[0] = solBest_0
    sol[1] = solBest_1
