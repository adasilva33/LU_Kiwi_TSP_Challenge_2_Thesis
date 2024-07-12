# -*- coding: utf-8 -*-
"""
Created on Sat Jul 27 13:08:55 2019

@author: pylya
"""

import Operators

def Initial_Sol(start_air, areas_and_airports, mydict, areas_n):
    start_area = 0
    for i in range(areas_n):
        if start_air in areas_and_airports[i*2 + 1]:
            start_area = i
            break
    solArea = list(range(areas_n + 1))
    Operators.Swap(solArea, 0, start_area)
    solArea[areas_n] = start_area
    
    solAirport = [start_air]
    for i in range(1,areas_n + 1):
        solAirport.append(areas_and_airports[solArea[i]*2 + 1][0])
    
    return solArea, solAirport

def CalculateFeasibiity(sol,mydict, areas_n):
    feas = 0
    indexes = []
    for i in range(areas_n):
        if ((sol[1][i],sol[1][i+1],i+1)) in mydict.keys() or ((sol[1][i],sol[1][i+1],0)) in mydict.keys():
            next
        else:
            feas = feas + 1
            if i > 0 and i < areas_n:
                indexes.append(i)
    if len(indexes) == 0:
        return feas, 1, areas_n - 2
    else:
        ix = min(indexes)
        ixx = max(indexes)
    return feas, ix, ixx

def PFeas(sol,mydict, areas_n,x,y,Rev,CAL):
    feas = 0
    if CAL == True:
        if ((sol[1][x-1],sol[1][x],x)) not in mydict.keys() and ((sol[1][x-1],sol[1][x],0)) not in mydict.keys():
            feas += 1
            return feas
        if ((sol[1][x],sol[1][x+1],x+1)) not in mydict.keys() and ((sol[1][x],sol[1][x+1],0)) not in mydict.keys():
            feas += 1
            return feas
        if ((sol[1][y-1],sol[1][y],y)) not in mydict.keys() and ((sol[1][y-1],sol[1][y],0)) not in mydict.keys():
            feas += 1
            return feas
    else:
        if Rev == False:
            if ((sol[1][x-1],sol[1][x],x)) not in mydict.keys() and ((sol[1][x-1],sol[1][x],0)) not in mydict.keys():
                feas += 1
                return feas
            if ((sol[1][x],sol[1][x+1],x+1)) not in mydict.keys() and ((sol[1][x],sol[1][x+1],0)) not in mydict.keys():
                feas += 1
                return feas
            if ((sol[1][y-1],sol[1][y],y)) not in mydict.keys() and ((sol[1][y-1],sol[1][y],0)) not in mydict.keys():
                feas += 1
                return feas
            if ((sol[1][y],sol[1][y+1],y+1)) not in mydict.keys() and ((sol[1][y],sol[1][y+1],0)) not in mydict.keys():
                feas += 1
                return feas
        else:
            if x > y:
                t = x
                x = y
                y = t
            for i in range(x-2,y+1): #range(x-2,y+1)
                if ((sol[1][i],sol[1][i+1],i+1)) not in mydict.keys() and ((sol[1][i],sol[1][i+1],0)) not in mydict.keys():
                    feas += 1
                    return feas
    return feas
        

def CalculateCost(sol,mydict, areas_n):
    cost = 0
    for i in range(areas_n):
        if ((sol[1][i],sol[1][i+1],i+1)) in mydict.keys():
            temp1 = mydict[(sol[1][i],sol[1][i+1],i+1)]
        else:
            temp1 = 500000
        if ((sol[1][i],sol[1][i+1],0)) in mydict.keys():
            temp2 = mydict[(sol[1][i],sol[1][i+1],0)]
        else:
            temp2 = 500000
        if temp1 < temp2:
            cost += temp1
        else:
            cost += temp2
    return cost

def PCost(sol,mydict, areas_n,x,y,Rev,CAL):
    cost = 0
    pen = 500000
    if CAL == True:
        if ((sol[1][x-1],sol[1][x],x)) in mydict.keys():
            temp1 = mydict[(sol[1][x-1],sol[1][x],x)]
        else:
            temp1 = pen
        if ((sol[1][x-1],sol[1][x],0)) in mydict.keys():
            temp2 = mydict[(sol[1][x-1],sol[1][x],0)]
        else:
            temp2 = pen
        if temp1 < temp2:
            cost += temp1
        else:
            cost += temp2
        if ((sol[1][x],sol[1][x+1],x+1)) in mydict.keys():
            temp1 = mydict[(sol[1][x],sol[1][x+1],x+1)]
        else:
            temp1 = pen
        if ((sol[1][x],sol[1][x+1],0)) in mydict.keys():
            temp2 = mydict[(sol[1][x],sol[1][x+1],0)]
        else:
            temp2 = pen
        if temp1 < temp2:
            cost += temp1
        else:
            cost += temp2
        if ((sol[1][y-1],sol[1][y],y)) in mydict.keys():
            temp1 = mydict[(sol[1][y-1],sol[1][y],y)]
        else:
            temp1 = pen
        if ((sol[1][y-1],sol[1][y],0)) in mydict.keys():
            temp2 = mydict[(sol[1][y-1],sol[1][y],0)]
        else:
            temp2 = pen
        if temp1 < temp2:
            cost += temp1
        else:
            cost += temp2
    else:
        if Rev == False:
            if ((sol[1][x-1],sol[1][x],x)) in mydict.keys():
                temp1 = mydict[(sol[1][x-1],sol[1][x],x)]
            else:
                temp1 = pen
            if ((sol[1][x-1],sol[1][x],0)) in mydict.keys():
                temp2 = mydict[(sol[1][x-1],sol[1][x],0)]
            else:
                temp2 = pen
            if temp1 < temp2:
                cost += temp1
            else:
                cost += temp2
            if ((sol[1][x],sol[1][x+1],x+1)) in mydict.keys():
                temp1 = mydict[(sol[1][x],sol[1][x+1],x+1)]
            else:
                temp1 = pen
            if ((sol[1][x],sol[1][x+1],0)) in mydict.keys():
                temp2 = mydict[(sol[1][x],sol[1][x+1],0)]
            else:
                temp2 = pen
            if temp1 < temp2:
                cost += temp1
            else:
                cost += temp2
            if ((sol[1][y-1],sol[1][y],y)) in mydict.keys():
                temp1 = mydict[(sol[1][y-1],sol[1][y],y)]
            else:
                temp1 = pen
            if ((sol[1][y-1],sol[1][y],0)) in mydict.keys():
                temp2 = mydict[(sol[1][y-1],sol[1][y],0)]
            else:
                temp2 = pen
            if temp1 < temp2:
                cost += temp1
            else:
                cost += temp2
            if ((sol[1][y],sol[1][y+1],y+1)) in mydict.keys():
                temp1 = mydict[(sol[1][y],sol[1][y+1],y+1)]
            else:
                temp1 = pen
            if ((sol[1][y],sol[1][y+1],0)) in mydict.keys():
                temp2 = mydict[(sol[1][y],sol[1][y+1],0)]
            else:
                temp2 = pen
            if temp1 < temp2:
                cost += temp1
            else:
                cost += temp2
        else:
            if x > y:
                t = x
                x = y
                y = t
            for i in range(x-2,y+1): #range(x-2,y+1)
                if ((sol[1][i],sol[1][i+1],i+1)) in mydict.keys():
                    temp1 = mydict[(sol[1][i],sol[1][i+1],i+1)]
                else:
                    temp1 = pen
                if ((sol[1][i],sol[1][i+1],0)) in mydict.keys():
                    temp2 = mydict[(sol[1][i],sol[1][i+1],0)]
                else:
                    temp2 = pen
                if temp1 < temp2:
                    cost += temp1
                else:
                    cost += temp2
    return cost