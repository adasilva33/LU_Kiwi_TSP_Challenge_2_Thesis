# -*- coding: utf-8 -*-
"""
Created on Sat Jul 27 13:16:35 2019

@author: pylya
"""

import numpy as np
import Operators
import Calculations

def ImproveFeasibility(sol, areas_and_airports, mydict, areas_n):
    LLH0 = lambda: Operators.Swap2(sol[0],sol[1],x,feas[1])
    LLH1 = lambda: Operators.Swap2(sol[0],sol[1],x,feas[2])
    LLH5 = lambda: Operators.Reverse(sol[0],sol[1],feas[1],yy)
    LLHS = [LLH0,LLH1,LLH5]
    feas = list(Calculations.CalculateFeasibiity(sol,mydict,areas_n))
    #feedback = []
    while feas[0] != 0:
        x = np.random.randint(1,areas_n)
        if feas[2] == feas[1]:
            yy = feas[1]
        else:
            yy = np.random.randint(feas[1],feas[2])
        l = np.random.randint(0,len(LLHS))
        #air = [sol[1][feas[1]], sol[1][yy], sol[1][x], sol[1][feas[2]+1]]
        copy_0 = sol[0].copy()
        copy_1 = sol[1].copy()
        LLHS[l]()
        Operators.Change_Airport(sol[1],sol[0],feas[1],yy,areas_and_airports)
        Operators.Change_Airport(sol[1],sol[0],x,feas[2]+1,areas_and_airports)
        feas_new = list(Calculations.CalculateFeasibiity(sol,mydict,areas_n))
        if feas_new[0] <= feas[0]:
            feas = feas_new
            #feedback.append(l)
        else:
            #LLHS[l]()
            sol[0] = copy_0
            sol[1] = copy_1
            #sol[1][feas[1]] = air[0]
            #sol[1][yy] = air[1]
            #sol[1][x] = air[2]
            #sol[1][feas[2]+1] = air[3]
    #print('LLH0 :',feedback.count(0))
    #print('LLH1 :',feedback.count(1))
    #print('LLH2 :',feedback.count(2))
    #print('LLH3 :',feedback.count(3))
    #print('LLH4 :',feedback.count(4))
    #print('LLH5 :',feedback.count(2))