import sys
sys.path.append('/usr/lib/python27/dist-packages/')
import pandas as pd
import numpy as np
import os
import math

arrayCumAct = np.loadtxt('../CumActivity/femme_j0.txt',skiprows=1)
x = arrayCumAct[:,0]
y = arrayCumAct[:,1]
ykL = arrayCumAct[:,2]
ySpleen = arrayCumAct[:,3]
yLiver = arrayCumAct[:,4]

R_kidneyCumAct = (np.trapz(y,x,axis=0) + y[4]*np.exp(-x[4]*(np.log(2)/(6.6457*24))))*math.pow(10,6)*3600
L_kidneyCumAct = (np.trapz(ykL,x,axis=0) + ykL[4]*np.exp(-x[4]*(np.log(2)/(6.6457*24))))*math.pow(10,6)*3600
liverCumAct = (np.trapz(yLiver,x,axis=0) + yLiver[4]*np.exp(-x[4]*(np.log(2)/(6.6457*24))))*math.pow(10,6)*3600
spleenCumAct = (np.trapz(ySpleen,x,axis=0) + ySpleen[4]*np.exp(-x[4]*(np.log(2)/(6.6457*24))))*math.pow(10,6)*3600
kidneysCumAct = R_kidneyCumAct+L_kidneyCumAct

print 'Cumulated Activities' 
print 'Right kidneys =', round(R_kidneyCumAct,2) , 'MBq.h'
print 'Left kidney = ', round(L_kidneyCumAct,2) , 'MBq.h'
print ' kidneys =' , round(kidneysCumAct,2), 'MBq.h'
print 'Liver = ', round(liverCumAct,2) , 'MBq.h'
print 'Spleen = ', round(spleenCumAct,2) , 'MBq.h'


choice = input('Which organ are we analysing? \n 1: liver \n 2: kidneys \n 3: spleen \n ')
if choice == 1:
	CT = 'data/cropedCT_patientF_j0.mhd'
        doseImage = 'output/Liver/Liver_betaMinus-Dose.mhd'
        doseUnc = 'output/Liver/Liver_betaMinus-Dose-Uncertainty.mhd'
        doseUncG = 'output/Liver/Liver_G-Dose-Uncertainty.mhd'
        doseUncX = 'output/Liver/Liver_X-Dose-Uncertainty.mhd'
        doseUncIE = 'output/Liver/Liver_IE-Dose-Uncertainty.mhd'
        doseUncAE = 'output/Liver/Liver_AE-Dose-Uncertainty.mhd'
        doseG = 'output/Liver/Liver_G-Dose.mhd'
        doseX = 'output/Liver/Liver_X-Dose.mhd'
        doseIE = 'output/Liver/Liver_IE-Dose.mhd'
        doseAE = 'output/Liver/Liver_AE-Dose.mhd'
	outName = 'liver'
        cumActivity = liverCumAct          #1.09993e15
elif choice == 2:
	CT = 'data/cropedCT_patientF_j0.mhd'
        doseImage = 'output/Kidneys/Kidneys_betaMinus-Dose.mhd'
        doseUnc = 'output/Kidneys/Kidneys_betaMinus-Dose-Uncertainty.mhd'
        doseUncG = 'output/Kidneys/Kidneys_G-Dose-Uncertainty.mhd'
        doseUncX = 'output/Kidneys/Kidneys_X-Dose-Uncertainty.mhd'
        doseUncIE = 'output/Kidneys/Kidneys_IE-Dose-Uncertainty.mhd'
        doseUncAE = 'output/Kidneys/Kidneys_AE-Dose-Uncertainty.mhd'
        doseG = 'output/Kidneys/Kidneys_G-Dose.mhd'
        doseX = 'output/Kidneys/Kidneys_X-Dose.mhd'
        doseIE = 'output/Kidneys/Kidneys_IE-Dose.mhd'
        doseAE = 'output/Kidneys/Kidneys_AE-Dose.mhd'
	outName = 'kidneys'
        cumActivity = kidneysCumAct              #4.21254e13

elif choice == 3:
	CT = 'data/cropedCT_patientF_j0.mhd'
        doseImage = 'output/Spleen/Spleen_betaMinus-Dose.mhd'
        doseUnc = 'output/Spleen/Spleen_betaMinus-Dose-Uncertainty.mhd'
        doseUncG = 'output/Spleen/Spleen_G-Dose-Uncertainty.mhd'
        doseUncX = 'output/Spleen/Spleen_X-Dose-Uncertainty.mhd'
        doseUncIE = 'output/Spleen/Spleen_IE-Dose-Uncertainty.mhd'
        doseUncAE = 'output/Spleen/Spleen_AE-Dose-Uncertainty.mhd'
        doseG = 'output/Spleen/Spleen_G-Dose.mhd'
        doseX = 'output/Spleen/Spleen_X-Dose.mhd'
        doseIE = 'output/Spleen/Spleen_IE-Dose.mhd'
        doseAE = 'output/Spleen/Spleen_AE-Dose.mhd'
	outName = 'spleen'
        cumActivity = spleenCumAct         #1.83526e13

else: print 'Not an avaiale option !!!'

fileKidneys="data/cropedKidneys.mhd"
fileSpleen="data/cropedSpleen.mhd"
fileLiver="data/cropedLiver.mhd"


# read GATE  mhd parameters

CT_array = np.fromfile(CT.replace('mhd','raw'), dtype=np.uint16)


########################################################################################
################################ read dose file  #######################################
########################################################################################

dose_mhd_param = pd.read_table(doseImage,header=None,sep=' = ',index_col=0,engine='python')
dose_voxel_size = map(float, dose_mhd_param.loc[['ElementSpacing']].values[0][0].split())
dose_voxel_volume = dose_voxel_size[0]*dose_voxel_size[1]*dose_voxel_size[2]/1000
dose_dim_size = map(int, dose_mhd_param.loc[['DimSize']].values[0][0].split())
dose_nb_voxels = dose_dim_size[0]*dose_dim_size[1]*dose_dim_size[2]

# get Dose 3D image (Dose is in Gy (J/kg))
doseArray = np.fromfile(doseImage.replace('mhd','raw'), dtype=np.float32)
#doseArray = doseArray.reshape(81,233,413)
if (len(doseArray) != dose_nb_voxels):
   print "Reading binary type incorrect"
else:
    print "Reading binary images ok!"

##################################################################################
############################### ORGANS MASKS #####################################
##################################################################################

mask_kidneys = np.fromfile(fileKidneys.replace('mhd','raw'), dtype=np.uint16)
mask_spleen = np.fromfile(fileSpleen.replace('mhd','raw'), dtype=np.uint16)
mask_liver = np.fromfile(fileLiver.replace('mhd','raw'), dtype=np.uint16)

##################################################################################
############################### PARTICLE TYPE ####################################
##################################################################################

doseBetaMinus = np.fromfile(doseImage.replace('mhd','raw'), dtype=np.float32)
doseArrayG = np.fromfile(doseG.replace('mhd','raw'), dtype=np.float32)
doseArrayX = np.fromfile(doseX.replace('mhd','raw'), dtype=np.float32)
doseArrayIE = np.fromfile(doseIE.replace('mhd','raw'), dtype=np.float32)
doseArrayAE = np.fromfile(doseAE.replace('mhd','raw'), dtype=np.float32)

# ------------------------- Uncertainties --------------------------------------
uncDoseBM = np.fromfile(doseUnc.replace('mhd','raw'), dtype=np.float32)
uncDoseG = np.fromfile(doseUncG.replace('mhd','raw'), dtype=np.float32)
uncDoseX = np.fromfile(doseUncX.replace('mhd','raw'), dtype=np.float32)
uncDoseIE = np.fromfile(doseUncIE.replace('mhd','raw'), dtype=np.float32)
uncDoseAE = np.fromfile(doseUncAE.replace('mhd','raw'), dtype=np.float32)
# ------------------------------------------------------------------------------

bMinusEvents = 1e9
G_Events = 0.1803e9
X_Events = 1.374e9
IE_Events = 0.1548e9
AE_Events = 1.117e9

doseBetaMinus = doseBetaMinus/bMinusEvents
doseArrayG = doseArrayG/G_Events
doseArrayX = doseArrayG/X_Events
doseArrayIE = doseArrayG/IE_Events
doseArrayAE = doseArrayG/AE_Events

########################################################################################
############################     Start analysing       #################################
########################################################################################

# ------------- Organs masks -----
b_liver = (mask_liver==1)
b_kidneys = (mask_kidneys==1)
b_spleen = (mask_spleen==1)
# -------------------------------

# ----  Relative dose to Absolute dose ----
uncDoseBM = uncDoseBM * doseBetaMinus
uncDoseG = uncDoseG * doseArrayG
uncDoseX = uncDoseX * doseArrayX
uncDoseIE = uncDoseIE * doseArrayIE
uncDoseAE = uncDoseAE * doseArrayAE
# ----------------------------------------

# -------------------------------------- Sigma L I V E R -----------------------------------------------
sigmaDoseBM = np.sqrt((uncDoseBM[b_liver]**2).sum()) / b_liver.sum()
sigmaDoseG = np.sqrt((uncDoseG[b_liver]**2).sum()) / b_liver.sum()
sigmaDoseX = np.sqrt((uncDoseX[b_liver]**2).sum()) / b_liver.sum()
sigmaDoseIE = np.sqrt((uncDoseIE[b_liver]**2).sum()) / b_liver.sum()
sigmaDoseAE = np.sqrt((uncDoseAE[b_liver]**2).sum()) / b_liver.sum()

sigmaLiver = np.sqrt((sigmaDoseBM**2)+(sigmaDoseG**2)+(sigmaDoseX**2)+(sigmaDoseIE**2)+(sigmaDoseAE**2))
# -------------------------------------------------------------------------------------------------------

# --------------------------------------- Sigma K I D N E Y S ------------------------------------------
kidneys_sigmaDoseBM = np.sqrt((uncDoseBM[b_kidneys]**2).sum())/b_kidneys.sum()
kidneys_sigmaDoseG = np.sqrt((uncDoseG[b_kidneys]**2).sum())/b_kidneys.sum()
kidneys_sigmaDoseX = np.sqrt((uncDoseX[b_kidneys]**2).sum())/b_kidneys.sum()
kidneys_sigmaDoseIE = np.sqrt((uncDoseIE[b_kidneys]**2).sum())/b_kidneys.sum()
kidneys_sigmaDoseAE = np.sqrt((uncDoseAE[b_kidneys]**2).sum())/b_kidneys.sum()

sigmaKidneys = np.sqrt((kidneys_sigmaDoseBM**2)+(kidneys_sigmaDoseG**2)+(kidneys_sigmaDoseX**2)+(kidneys_sigmaDoseIE**2)+(kidneys_sigmaDoseAE**2))
# ------------------------------------------------------------------------

# ----------------------- Sigma S P L E E N -----------------------------
spleen_sigmaDoseBM = np.sqrt((uncDoseBM[b_spleen]**2).sum())/b_spleen.sum()
spleen_sigmaDoseG = np.sqrt((uncDoseG[b_spleen]**2).sum())/b_spleen.sum()
spleen_sigmaDoseX = np.sqrt((uncDoseX[b_spleen]**2).sum())/b_spleen.sum()
spleen_sigmaDoseIE = np.sqrt((uncDoseIE[b_spleen]**2).sum())/b_spleen.sum()
spleen_sigmaDoseAE = np.sqrt((uncDoseAE[b_spleen]**2).sum())/b_spleen.sum()

sigmaSpleen = np.sqrt((spleen_sigmaDoseBM**2)+(spleen_sigmaDoseG**2)+(spleen_sigmaDoseX**2)+(spleen_sigmaDoseIE**2)+(spleen_sigmaDoseAE**2))
# -----------------------------------------------------------------------


#print mask_liver.sum()
#print doseArray[b_maskArray].sum(), b_maskArray.dtype
#print b_liver.sum()


doseArrayT = doseBetaMinus + doseArrayX + doseArrayG + doseArrayIE + doseArrayAE
#print 'Dose total' ,doseArrayT.sum()
outFile = open('output/'+outName+'SourceDose.txt','w+')
print >> outFile,  'Dose liver', doseArrayT[b_liver].sum()/b_liver.sum()*cumActivity, '+-', sigmaLiver*cumActivity , '(',round((sigmaLiver*cumActivity)/(doseArrayT[b_liver].sum()/b_liver.sum()*cumActivity)*100,2),'%)'
print >> outFile, 'Dose kidneys', doseArrayT[b_kidneys].sum()/b_kidneys.sum()*cumActivity ,'+-', sigmaKidneys*cumActivity, '(', round(sigmaKidneys/(doseArrayT[b_kidneys].sum()/b_kidneys.sum())*100,2), '%)'
#print 'Dose kidneys (beta)', doseBetaMinus[b_kidneys].sum()/b_kidneys.sum()*1.09993e15
print >> outFile, 'Dose spleen', doseArrayT[b_spleen].sum()/b_spleen.sum()*cumActivity , '+-' , sigmaSpleen*cumActivity, '(', round(sigmaSpleen/(doseArrayT[b_spleen].sum()/b_spleen.sum())*100,2), '%)'

#print np.amin(CT_array[b_maskArray])
#print np.amax(CT_array[b_maskArray])
#doseBetaM = doseBetaMinus[b_liver].sum()/b_liver.sum()
#dose_target = doseArrayT[b_liver].sum()/b_liver.sum()
#print 'Total absorbed dose', dose_target*1.09993e15
#print 'Beta minus aborbed dose', doseBetaM*1.09993e15
print >> outFile, ' '
print >> outFile, '****************  Organs Volumes and Masses ****************'
print >> outFile, ' '
print >> outFile, 'Liver volume', 0.976562 * 0.976562 * 5 * b_liver.sum()/1000, 'ml'
print >> outFile, 'Liver mass', 1.0616 * 0.976562 * 0.976562 * 5 * b_liver.sum()/1000, 'g' 
print >> outFile, ' '
print >> outFile, 'Kidnyes volume', 0.976562 * 0.976562 * 5 * b_kidneys.sum()/1000, 'ml'
print >> outFile, 'Kidneys mass', 1.0616 * 0.976562 * 0.976562 * 5 * b_kidneys.sum()/1000 , 'g'
print >> outFile, ' '
print >> outFile, 'Spleen volume', 0.976562 * 0.976562 * 5 * b_spleen.sum()/1000, 'ml'
print >> outFile, 'Spleen mass', 1.0616 * 0.976562 * 0.976562 * 5 * b_spleen.sum()/1000, 'g' 
outFile.close()
