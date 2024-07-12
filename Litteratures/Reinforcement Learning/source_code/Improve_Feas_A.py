# -*- coding: utf-8 -*-
"""
Created on Sat Jul 27 13:16:35 2019

@author: pylya
"""

import numpy as np
import Operators
import Calculations

def ImproveFeasibility(sol, areas_and_airports, mydict, areas_n):
    LLH0 = lambda: Operators.Swap2(sol[0],sol[1],x,y)
    LLH1 = lambda: Operators.Insert(sol[0],sol[1],x,y)
    LLH2 = lambda: Operators.Swap2(sol[0],sol[1],x,yy)
    LLH3 = lambda: Operators.Insert(sol[0],sol[1],x,yy)
    LLHS = [LLH0,LLH1,LLH2,LLH3]
    feas = list(Calculations.CalculateFeasibiity(sol,mydict,areas_n))
    while feas[0] != 0:
        x = np.random.randint(1,areas_n)
        yy = np.random.randint(feas[1],feas[2]+1)
        y = np.random.randint(1,areas_n)
        l = np.random.randint(0,len(LLHS))
        copy_0 = sol[0].copy()
        copy_1 = sol[1].copy()
        LLHS[l]()
        Operators.Change_Airport(sol[1],sol[0],x,feas[2],areas_and_airports)
        Operators.Change_Airport(sol[1],sol[0],x,feas[2]+1,areas_and_airports)
        feas_new = list(Calculations.CalculateFeasibiity(sol,mydict,areas_n))
        if feas_new[0] <= feas[0]:
            feas = feas_new
        else:
            sol[0] = copy_0
            sol[1] = copy_1
            