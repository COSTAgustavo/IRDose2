import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import glob
import math

arrayCumAct = np.loadtxt('femme_j0.txt',skiprows=1)
x = arrayCumAct[:,0]
y = arrayCumAct[:,1]
fig = plt.figure() 
plt.plot(x,y,'--v',color='green', label='Atividade - Rim direito')
#plt.stem(x,y, '-')
plt.annotate('A1', xy=(0.2,3), xytext=(29,8),color='green',
	     arrowprops=dict(color='green', arrowstyle="->", linestyle='dashed'), 
	     )
		#plt.plot(x,yW,'--v', label='Water Centre')
		#plt.plot(x,yWO,'--P', label= 'Water Off Centre')
		##plt.grid(axis='y', linestyle='-')
		#plt.grid(linestyle='-')
		##plt.show()
plt.ylabel('Acitvity (MBq)')
plt.xlabel('Time (h)')
#plt.fill(x,y,color='0.8')
plt.fill_between(x,0,y, color='0.8')
plt.vlines(x,0,y,linestyle='dashed')
plt.text(8,30,'A2', color='green')
plt.text(43,18,'A3', color='green')
plt.text(127,6,'A4', color='green')
plt.legend()
#plt.title(enWind[n]+' keV')
plt.savefig('cumActivity.png')
#np.delete(yA,2)
#np.delete(arrayAir,2)
plt.close(fig)

expX =  np.linspace(x[4],2000000,1000)
expY = y[4]*np.exp(-(expX*(np.log(2)/(6.624*24*3600))))
fig = plt.figure()
#my_xticks = [x[4], '$\infty$'] 
my_xticks = ['$t_5$', '$\infty$'] 
plt.xticks(x, my_xticks)

plt.plot(expX,expY,color='green', label='Atividade - Rim direito' )
plt.fill_between(expX,0,expY, color='0.8')
plt.ylabel('Atividade (MBq)')
plt.xlabel('Tempo (h)')
plt.xticks(np.arange(x[4], 2000000, 1999000))
plt.text(300000,2.5,'A5', color='green')
plt.text(600000,0.8,r'$\int_{t_5}^\infty A_5 e^{-\lambda t}\mathrm{d}t$', horizontalalignment='center', fontsize=20)
plt.legend()
#plt.title(enWind[n]+' keV')
plt.savefig('cumActivityExp.png')
#np.delete(yA,2)
#np.delete(arrayAir,2)
plt.close(fig)

cumActivity = (np.trapz(y,x,axis=0) + y[4]*np.exp(-x[4]*(np.log(2)/(6.6457*24))))*math.pow(10,6)*3600

print 'Cumulated Activity =', round(cumActivity,2) , 'MBq.h'




