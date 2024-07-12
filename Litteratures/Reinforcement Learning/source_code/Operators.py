# -*- coding: utf-8 -*-
"""
Created on Sat Jul 27 13:04:13 2019

@author: pylya
"""

import numpy as np

def Swap(arr,a,b):
    temp = arr[a]
    arr[a] = arr[b]
    arr[b] = temp

def Swap2(arr,arr2,a,b):
    temp = arr[a]
    temp2 = arr2[a]
    arr[a] = arr[b]
    arr2[a] = arr2[b]
    arr[b] = temp
    arr2[b] = temp2

def Reverse(arr,arr2,a,b):
    if a > b:
        t = a
        a = b
        b = t
    temp = arr
    temp2 = arr2
    c = a
    for i in temp[b:a:-1]:
        arr[a+1] = i
        a += 1
    for i in temp2[b:c:-1]:
        arr2[c+1] = i
        c += 1
        
def Insert(arr,arr2,a,b):
    temp = arr[a]
    temp2 = arr2[a]
    arr.remove(temp)
    arr2.remove(temp2)
    arr.insert(b,temp)
    arr2.insert(b,temp2)
       
def Change_Airport(arr,arr2,a,b,areas_and_airports):
    np.random.shuffle(areas_and_airports[arr2[a]*2 + 1])
    np.random.shuffle(areas_and_airports[arr2[b]*2 + 1])
    
    arr[a] = areas_and_airports[arr2[a]*2 + 1][0]
    arr[b] = areas_and_airports[arr2[b]*2 + 1][0]
    
def Swap_K(arr,arr2,a,areas_n):
    for i in range(a):
        s = np.random.randint(1,areas_n,size=a*2)
    for i in range((a//2)+2):
        temp = arr[s[i]]
        arr[s[i]] = arr[s[i+1]]
        arr[s[i+1]] = temp
        temp2 = arr2[s[i]]
        arr2[s[i]] = arr2[s[i+1]]
        arr2[s[i+1]] = temp2