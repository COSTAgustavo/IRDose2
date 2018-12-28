import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import glob
import math

arrayCumAct = np.loadtxt('femme_j0.txt',skiprows=1)
x = arrayCumAct[:,0]
y = arrayCumAct[:,1]
ykL = arrayCumAct[:,2]
ySpleen = arrayCumAct[:,3]
yLiver = arrayCumAct[:,4]

R_kidneyCumAct = (np.trapz(y,x,axis=0) + y[4]*np.exp(-x[4]*(np.log(2)/(6.6457*24))))*math.pow(10,6)*3600
L_kidneyCumAct = (np.trapz(ykL,x,axis=0) + ykL[4]*np.exp(-x[4]*(np.log(2)/(6.6457*24))))*math.pow(10,6)*3600
liverCumAct = (np.trapz(yLiver,x,axis=0) + yLiver[4]*np.exp(-x[4]*(np.log(2)/(6.6457*24)))/ (np.log(2)/(6.6457*24)) )*math.pow(10,6)*3600
spleenCumAct = (np.trapz(ySpleen,x,axis=0) + ySpleen[4]*np.exp(-x[4]*(np.log(2)/(6.6457*24))))*math.pow(10,6)*3600

print 'Cumulated Activities'
print 'Right kidneys =', round(R_kidneyCumAct,2) , 'MBq.h'
print 'Left kidney = ', round(L_kidneyCumAct,2) , 'MBq.h'
print ' kidneys =' , round(R_kidneyCumAct+L_kidneyCumAct,2), 'MBq.h'
print 'Liver = ', round(liverCumAct,2) , 'MBq.h'
print 'Spleen = ', round(spleenCumAct,2) , 'MBq.h'





