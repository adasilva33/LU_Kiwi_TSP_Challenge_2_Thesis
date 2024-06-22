# -*- coding: utf-8 -*-
"""
Created on Sat Jul 27 12:59:05 2019

@author: pylya
"""

import Calculations

def ReadFile(f_name):
    dist = []
    line_nu = -1
    with open(f_name) as infile:
        for line in infile:
            line_nu += 1
            if line_nu == 0:
                index = int(line.split()[0]) * 2 + 1
            if line_nu >= index:
                temp = line.split()
                temp[2] = int(temp[2])
                temp[3] = int(temp[3])
                dist.append(temp)
            else:
                dist.append(line.split())
        info = dist[0:int(dist[0][0])*2+1]
        flights = dist[int(dist[0][0])*2+1:]
    return info, flights

def CreateDistances(File, areas_n):
    mydict = {}
    for i in File:
        if ((i[0],i[1],i[2])) in mydict.keys():
            if mydict[(i[0],i[1],i[2])] > i[3]:
                mydict[(i[0],i[1],i[2])] = i[3]
        else:
            mydict[(i[0],i[1],i[2])] = i[3]
    return mydict

def SaveFile(sol,mydict,areas_n):
    with open('mysol.csv', 'a') as writeFile:
        writeFile.write(str(Calculations.CalculateCost(sol,mydict, areas_n)))
        writeFile.write('\n')
        
def SaveUR(uti,uti_total):
    ops = ['swap-g.csv','swap-gg.csv','insert.csv','swap.csv']
    u = [round((uti.count(0)/uti_total*100),2),round((uti.count(1)/uti_total*100),2),round((uti.count(2)/uti_total*100),2),round((uti.count(3)/uti_total*100),2)]
    for i in range(len(ops)):
        with open(ops[i], 'a') as writeFile:
            writeFile.write(str(u[i]))
            writeFile.write('\n')

def SaveCost(t,c):
    files = ['times.csv','costs.csv']
    var = [t,c]
    for i in range(len(files)):
        for j in range(len(c)):
            with open(files[i], 'a') as writeFile:
                writeFile.write(str(var[i][j]))
                writeFile.write('\n')
                
def Save_Feas(f,t,op):
    files = ['feasibility.csv','times.csv','operator.csv']
    var = [f,t,op]
    for i in range(len(files)):
        for j in range(len(var[i])):
            with open(files[i], 'a') as writeFile:
                writeFile.write(str(var[i][j]))
                writeFile.write('\n')
        