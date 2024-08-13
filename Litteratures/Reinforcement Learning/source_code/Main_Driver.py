# -*- coding: utf-8 -*-
"""
Created on Sat Jul 27 12:56:47 2019

@author: pylya
"""



import Read_File
import Calculations
import time
import Improve_Feas_A as IFeas
#Use Improve_Feas_A for Instances: {1,2,3,4,5,6,8,10}
#Use Improve_Feas_B for Instances: {7}
#Use Improve_Feas_C for Instances: {9,11,12,13}
#Use Improve_Feas_D for Instances: {14}
import RL_OI as Method
#Methods available: {SR_IE, RD, RP_IE, RPD, SR_GD, RL_OI}

start_time = time.time()
#Type below the maximum time allowed (i.e. 2.99, 4.99, 14.99)
run_time = 14.99
#Type below the problem instance (i.e. "1.in", "2.in", etc.)
File = Read_File.ReadFile("/Users/adslv/Documents/LU/Term 3/Kiwi_TSP_Challenge/Litteratures/Reinforcement Learning/source_code/Flight connections dataset/6.in") 

areas_n = int(File[0][0][0])
start_air = File[0][0][1]
areas_and_airports = File[0][1:]
mydict = Read_File.CreateDistances(File[1], areas_n)
#print(mydict)
sol = list(Calculations.Initial_Sol(start_air, areas_and_airports, mydict, areas_n))
print(sol)
IFeas.ImproveFeasibility(sol, areas_and_airports, mydict, areas_n)
print(sol)
Method.HH(sol, areas_and_airports, mydict, areas_n, start_time, run_time)
print('Run Time: ', time.time() - start_time)
print('Feasibility :',Calculations.CalculateFeasibiity(sol,mydict, areas_n)[0])
print('Total Cost :',Calculations.CalculateCost(sol,mydict, areas_n))
print("Solution areas: ", sol[0])
print("Solution airports: ", sol[1])