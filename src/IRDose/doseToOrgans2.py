import sys
#sys.path.append('/usr/lib/python27/dist-packages/')
import pandas as pd
#### usage : python doseToOrgans.py organName True True -- or False

import numpy as np
import os
import math

argName = sys.argv[1]
target_1 = sys.argv[2]
target_2 = sys.argv[3]



CT = 'dosimetrie/stdGATE/data/'+argName+'.mhd'
doseImage = 'dosimetrie/stdGATE/output/'+argName+'/'+argName+'_betaMinus-Dose.mhd'
doseUnc = 'dosimetrie/stdGATE/output/'+argName+'/'+argName+'_betaMinus-Dose-Uncertainty.mhd'
doseUncG = 'dosimetrie/stdGATE/output/'+argName+'/'+argName+'_G-Dose-Uncertainty.mhd'
doseUncX = 'dosimetrie/stdGATE/output/'+argName+'/'+argName+'_X-Dose-Uncertainty.mhd'
doseUncIE = 'dosimetrie/stdGATE/output/'+argName+'/'+argName+'_IE-Dose-Uncertainty.mhd'
doseUncAE = 'dosimetrie/stdGATE/output/'+argName+'/'+argName+'_AE-Dose-Uncertainty.mhd'
doseG = 'dosimetrie/stdGATE/output/'+argName+'/'+argName+'_G-Dose.mhd'
doseX = 'dosimetrie/stdGATE/output/'+argName+'/'+argName+'_X-Dose.mhd'
doseIE = 'dosimetrie/stdGATE/output/'+argName+'/'+argName+'_IE-Dose.mhd'
doseAE = 'dosimetrie/stdGATE/output/'+argName+'/'+argName+'_AE-Dose.mhd'

cumActivity = 8.68010783453e14          #1.09993e15

fileSource='dosimetrie/stdGATE/data/'+argName+'_source.mhd'
if target_1=='True':
   fileTarget_1='dosimetrie/stdGATE/data/'+argName+'_target_1.mhd'
if target_2=='True':
   fileTarget_2='dosimetrie/stdGATE/data/'+argName+'_target_2.mhd'


# read GATE  mhd parameters

CT_array = np.fromfile(CT.replace('mhd','raw'), dtype=np.uint16)


########################################################################################
################################ read dose file  #######################################
########################################################################################

#dose_mhd_param = pd.read_table(doseImage,header=None,sep=' = ',index_col=0,engine='python')
#dose_voxel_size = map(float, dose_mhd_param.loc[['ElementSpacing']].values[0][0].split())
#dose_voxel_volume = dose_voxel_size[0]*dose_voxel_size[1]*dose_voxel_size[2]/1000
#dose_dim_size = map(int, dose_mhd_param.loc[['DimSize']].values[0][0].split())
#dose_nb_voxels = dose_dim_size[0]*dose_dim_size[1]*dose_dim_size[2]

# get Dose 3D image (Dose is in Gy (J/kg))
doseArray = np.fromfile(doseImage.replace('mhd','raw'), dtype=np.float32)
#doseArray = doseArray.reshape(81,233,413)
#if (len(doseArray) != dose_nb_voxels):
#   print("Reading binary type incorrect")
#else:
#    print("Reading binary images ok!")

##################################################################################
############################### ORGANS MASKS #####################################
##################################################################################

mask_source = np.fromfile(fileSource.replace('mhd','raw'), dtype=np.uint16)
if target_1=='True':
    mask_target_1 = np.fromfile(fileTarget_1.replace('mhd','raw'), dtype=np.uint16)
if target_2=='True':
    mask_target_2 = np.fromfile(fileTarget_2.replace('mhd','raw'), dtype=np.uint16)

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

bMinusEvents = 1e5
G_Events = 0.1803e5
X_Events = 1.374e5
IE_Events = 0.1548e5
AE_Events = 1.117e5

doseBetaMinus = doseBetaMinus/bMinusEvents
doseArrayG = doseArrayG/G_Events
doseArrayX = doseArrayG/X_Events
doseArrayIE = doseArrayG/IE_Events
doseArrayAE = doseArrayG/AE_Events

########################################################################################
############################     Start analysing       #################################
########################################################################################

# ------------- Organs masks -----
b_source = (mask_source==1)
if target_1=='True':
    b_target_1 = (mask_target_1==1)
if target_2=='True':
    b_target_2 = (mask_target_2==1)
# -------------------------------

# ----  Relative dose to Absolute dose ----
uncDoseBM = uncDoseBM * doseBetaMinus
uncDoseG = uncDoseG * doseArrayG
uncDoseX = uncDoseX * doseArrayX
uncDoseIE = uncDoseIE * doseArrayIE
uncDoseAE = uncDoseAE * doseArrayAE
# ----------------------------------------

# -------------------------------------- Sigma S O U R C E -----------------------------------------------
sigmaDoseBM = np.sqrt((uncDoseBM[b_source]**2).sum()) / b_source.sum()
sigmaDoseG = np.sqrt((uncDoseG[b_source]**2).sum()) / b_source.sum()
sigmaDoseX = np.sqrt((uncDoseX[b_source]**2).sum()) / b_source.sum()
sigmaDoseIE = np.sqrt((uncDoseIE[b_source]**2).sum()) / b_source.sum()
sigmaDoseAE = np.sqrt((uncDoseAE[b_source]**2).sum()) / b_source.sum()

sigmaSource = np.sqrt((sigmaDoseBM**2)+(sigmaDoseG**2)+(sigmaDoseX**2)+(sigmaDoseIE**2)+(sigmaDoseAE**2))
# -------------------------------------------------------------------------------------------------------

# --------------------------------------- Sigma T A R G E T  1 ------------------------------------------
if target_1=='True':
    target_1_sigmaDoseBM = np.sqrt((uncDoseBM[b_target_1]**2).sum())/b_target_1.sum()
    target_1_sigmaDoseG = np.sqrt((uncDoseG[b_target_1]**2).sum())/b_target_1.sum()
    target_1_sigmaDoseX = np.sqrt((uncDoseX[b_target_1]**2).sum())/b_target_1.sum()
    target_1_sigmaDoseIE = np.sqrt((uncDoseIE[b_target_1]**2).sum())/b_target_1.sum()
    target_1_sigmaDoseAE = np.sqrt((uncDoseAE[b_target_1]**2).sum())/b_target_1.sum()

    sigmaTarget_1 = np.sqrt((target_1_sigmaDoseBM**2)+(target_1_sigmaDoseG**2)+(target_1_sigmaDoseX**2)+(target_1_sigmaDoseIE**2)+(target_1_sigmaDoseAE**2))
# ------------------------------------------------------------------------

# ----------------------- Sigma T A R G E T  2 -----------------------------
if target_2=='True':
    target_2_sigmaDoseBM = np.sqrt((uncDoseBM[b_target_2]**2).sum())/b_target_2.sum()
    target_2_sigmaDoseG = np.sqrt((uncDoseG[b_target_2]**2).sum())/b_target_2.sum()
    target_2_sigmaDoseX = np.sqrt((uncDoseX[b_target_2]**2).sum())/b_target_2.sum()
    target_2_sigmaDoseIE = np.sqrt((uncDoseIE[b_target_2]**2).sum())/b_target_2.sum()
    target_2_sigmaDoseAE = np.sqrt((uncDoseAE[b_target_2]**2).sum())/b_target_2.sum()

    sigmaTarget_2 = np.sqrt((target_2_sigmaDoseBM**2)+(target_2_sigmaDoseG**2)+(target_2_sigmaDoseX**2)+(target_2_sigmaDoseIE**2)+(target_2_sigmaDoseAE**2))
# -----------------------------------------------------------------------


doseArrayT = doseBetaMinus + doseArrayX + doseArrayG + doseArrayIE + doseArrayAE
outFile = open('dosimetrie/stdGATE/output/'+argName+'SourceDose.txt','w+')

print('Dose Source', doseArrayT[b_source].sum()/b_source.sum()*cumActivity, '+-', sigmaSource*cumActivity , '(',round((sigmaSource*cumActivity)/(doseArrayT[b_source].sum()/b_source.sum()*cumActivity)*100,2),'%)', file=outFile)
print('Dose Source', doseArrayT[b_source].sum()/b_source.sum()*cumActivity, '+-', sigmaSource*cumActivity , '(',round((sigmaSource*cumActivity)/(doseArrayT[b_source].sum()/b_source.sum()*cumActivity)*100,2),'%)')

if target_1=='True':
    print('Dose Target_1', doseArrayT[b_target_1].sum()/b_target_1.sum()*cumActivity ,'+-', sigmaTarget_1*cumActivity, '(', round(sigmaTarget_1/(doseArrayT[b_target_1].sum()/b_target_1.sum())*100,2), '%)', file=outFile)
    print('Dose Target_1', doseArrayT[b_target_1].sum()/b_target_1.sum()*cumActivity ,'+-', sigmaTarget_1*cumActivity, '(', round(sigmaTarget_1/(doseArrayT[b_target_1].sum()/b_target_1.sum())*100,2), '%)')
if target_2=='True':
    print('Dose target_2', doseArrayT[b_target_2].sum()/b_target_2.sum()*cumActivity ,'+-', sigmaTarget_2*cumActivity, '(', round(sigmaTarget_2/(doseArrayT[b_target_2].sum()/b_target_2.sum())*100,2), '%)', file=outFile)
    print('Dose target_2', doseArrayT[b_target_2].sum()/b_target_2.sum()*cumActivity ,'+-', sigmaTarget_2*cumActivity, '(', round(sigmaTarget_2/(doseArrayT[b_target_2].sum()/b_target_2.sum())*100,2), '%)')

outFile.close()
