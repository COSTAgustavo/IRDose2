import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
import os
import glob
import math

arrayCumAct = np.loadtxt('xcatOrgans.txt',skiprows=1)
x = arrayCumAct[:,0]
yLiver = arrayCumAct[:,1]
yk = arrayCumAct[:,2]
ySpleen = arrayCumAct[:,3]

arrayCumAct[:,1:4]
#print(arr)
kidneysCumAct = (np.trapz(yk,x,axis=0) + yk[4]*np.exp(-x[4]*(np.log(2)/(6.6457*24))) / (np.log(2)/(6.6457*24)) )*math.pow(10,6)*3600
liverCumAct = (np.trapz(yLiver,x,axis=0) + yLiver[4]*np.exp(-x[4]*(np.log(2)/(6.6457*24))) / (np.log(2)/(6.6457*24)) )*math.pow(10,6)*3600
spleenCumAct = ( np.trapz(ySpleen,x,axis=0) + ySpleen[4]*np.exp( -x[4]* (np.log(2)/(6.6457*24) ) ) / (np.log(2)/(6.6457*24)) )*math.pow(10,6)*3600

print 'Cumulated Activities'
print 'Kidneys =' , round(kidneysCumAct*5,2), 'MBq.h'
print 'Liver = ', round(liverCumAct*5,2) , 'MBq.h'
print 'Spleen = ', round(spleenCumAct*5,2) , 'MBq.h'
 

#outFile = open('xcatQuantOrgans.txt', 'w+')
#print(arr, file=outFile)

