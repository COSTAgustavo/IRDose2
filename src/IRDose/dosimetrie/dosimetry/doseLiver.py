import sys
sys.path.append('/usr/lib/python27/dist-packages/')
import pandas as pd
import numpy as np
import vtkDICOMPython
import vtk
import matplotlib.pyplot as plt

choice = input('Which organ are we analysing? \n 1: liver \n 2: kidneys \n 3: spleen \n ')
if choice == 1:
	CT = 'data/cropedCT_patientF_j0.mhd'
        doseImage = 'output/liver_betaMinus-Dose.mhd'
        doseUnc = 'output/liver_betaMinus-Dose-Uncertainty.mhd'
        doseUncG = 'output/liver_G-Dose-Uncertainty.mhd'
        doseUncX = 'output/liver_X-Dose-Uncertainty.mhd'
        doseUncIE = 'output/liver_IE-Dose-Uncertainty.mhd'
        doseUncAE = 'output/liver_AE-Dose-Uncertainty.mhd'
        doseG = 'output/liver_G-Dose.mhd'
        doseX = 'output/liver_X-Dose.mhd'
        doseIE = 'output/liver_IE-Dose.mhd'
        doseAE = 'output/liver_AE-Dose.mhd'
	outName = 'liver'
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
elif choice == 3:
	CT = 'data/cropedCT_patientF_j0.mhd'
        doseImage = 'output/liver_betaMinus-Dose.mhd'
        doseUnc = 'output/liver_betaMinus-Dose-Uncertainty.mhd'
        doseUncG = 'output/liver_G-Dose-Uncertainty.mhd'
        doseUncX = 'output/liver_X-Dose-Uncertainty.mhd'
        doseUncIE = 'output/liver_IE-Dose-Uncertainty.mhd'
        doseUncAE = 'output/liver_AE-Dose-Uncertainty.mhd'
        doseG = 'output/liver_G-Dose.mhd'
        doseX = 'output/liver_X-Dose.mhd'
        doseIE = 'output/liver_IE-Dose.mhd'
        doseAE = 'output/liver_AE-Dose.mhd'
	outName = 'liver'

else: print 'Not an avaiale option !!!'

fileKidneys="data/cropedKidneys.mhd"
fileSpleen="data/cropedSpleen.mhd"
fileLiver="data/cropedLiver.mhd"


# read GATE  mhd parameters

CT_array = np.fromfile(CT.replace('mhd','raw'), dtype=np.uint16)


#mask_mhd = pd.read_table(mask,header=None,sep=' = ',index_col=0,engine='python')
##mask_voxel_size = map(float, mask_mhd.loc[['ElementSpacing']].values[0][0].split())
#mask_voxel_volume = mask_voxel_size[0]*mask_voxel_size[1]*mask_voxel_size[2]/1000
#mask_dim_size = map(int, mask_mhd.loc[['DimSize']].values[0][0].split())
#mask_nb_voxels = mask_dim_size[0]*mask_dim_size[1]*mask_dim_size[2]

#maskArray = np.fromfile(mask.replace('mhd','raw'), dtype=np.uint16)

# get Dose 3D image (Dose is in Gy (J/kg))

#if (len(maskArray) != mask_nb_voxels):
#    print "Reading binary type incorrect"
#else:
#    print "Reading binary images ok!"

#maskArray = maskArray.reshape(81,233,413)

########################################################################################
############################ read LUND  mhd parameters #################################
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
sigmaDoseBM = np.sqrt((uncDoseBM[b_liver].sum()**2).sum())/b_liver.sum()
sigmaDoseG = np.sqrt((uncDoseG[b_liver].sum()**2).sum())/b_liver.sum()
sigmaDoseX = np.sqrt((uncDoseX[b_liver].sum()**2).sum())/b_liver.sum()
sigmaDoseIE = np.sqrt((uncDoseIE[b_liver].sum()**2).sum())/b_liver.sum()
sigmaDoseAE = np.sqrt((uncDoseAE[b_liver].sum()**2).sum())/b_liver.sum()

sigmaLiver = np.sqrt((sigmaDoseBM**2)+(sigmaDoseG**2)+(sigmaDoseX**2)+(sigmaDoseIE**2)+(sigmaDoseAE**2))
# -------------------------------------------------------------------------------------------------------

# --------------------------------------- Sigma K I D N E Y S ------------------------------------------
kidneys_sigmaDoseBM = np.sqrt((uncDoseBM[b_kidneys].sum()**2).sum())/b_liver.sum()
kidneys_sigmaDoseG = np.sqrt((uncDoseG[b_kidneys].sum()**2).sum())/b_liver.sum()
kidneys_sigmaDoseX = np.sqrt((uncDoseX[b_kidneys].sum()**2).sum())/b_liver.sum()
kidneys_sigmaDoseIE = np.sqrt((uncDoseIE[b_kidneys].sum()**2).sum())/b_liver.sum()
kidneys_sigmaDoseAE = np.sqrt((uncDoseAE[b_kidneys].sum()**2).sum())/b_liver.sum()

sigmaKidneys = np.sqrt((kidneys_sigmaDoseBM**2)+(kidneys_sigmaDoseG**2)+(kidneys_sigmaDoseX**2)+(kidneys_sigmaDoseIE**2)+(kidneys_sigmaDoseAE**2))
# ------------------------------------------------------------------------

# ----------------------- Sigma S P L E E N -----------------------------
spleen_sigmaDoseBM = np.sqrt((uncDoseBM[b_spleen].sum()**2).sum())/b_liver.sum()
spleen_sigmaDoseG = np.sqrt((uncDoseG[b_spleen].sum()**2).sum())/b_liver.sum()
spleen_sigmaDoseX = np.sqrt((uncDoseX[b_spleen].sum()**2).sum())/b_liver.sum()
spleen_sigmaDoseIE = np.sqrt((uncDoseIE[b_spleen].sum()**2).sum())/b_liver.sum()
spleen_sigmaDoseAE = np.sqrt((uncDoseAE[b_spleen].sum()**2).sum())/b_liver.sum()

sigmaSpleen = np.sqrt((spleen_sigmaDoseBM**2)+(spleen_sigmaDoseG**2)+(spleen_sigmaDoseX**2)+(spleen_sigmaDoseIE**2)+(spleen_sigmaDoseAE**2))
# -----------------------------------------------------------------------


#print mask_liver.sum()
#print doseArray[b_maskArray].sum(), b_maskArray.dtype
#print b_liver.sum()


doseArrayT = doseBetaMinus + doseArrayX + doseArrayG + doseArrayIE + doseArrayAE
#print 'Dose total' ,doseArrayT.sum()
outFile = open(outName+'SourceDose.txt','w+')
print >> outFile,  'Dose liver', doseArrayT[b_liver].sum()/b_liver.sum()*1.09993e15, '+-', sigmaLiver*1.09993e15 , '(',round((sigmaLiver*1.09993e15)/(doseArrayT[b_liver].sum()/b_liver.sum()*1.09993e15)*100,2),'%)'
print >> outFile, 'Dose kidneys', doseArrayT[b_kidneys].sum()/b_kidneys.sum()*1.09993e15 ,'+-', sigmaKidneys*1.09993e15, '(', round(sigmaKidneys/(doseArrayT[b_kidneys].sum()/b_kidneys.sum())*100,2), '%)'
#print 'Dose kidneys (beta)', doseBetaMinus[b_kidneys].sum()/b_kidneys.sum()*1.09993e15
print >> outFile, 'Dose spleen', doseArrayT[b_spleen].sum()/b_spleen.sum()*1.09993e15 , '+-' , sigmaSpleen*1.09993e15, '(', round(sigmaSpleen/(doseArrayT[b_spleen].sum()/b_spleen.sum())*100,2), '%)'

#print np.amin(CT_array[b_maskArray])
#print np.amax(CT_array[b_maskArray])
#doseBetaM = doseBetaMinus[b_liver].sum()/b_liver.sum()
#dose_target = doseArrayT[b_liver].sum()/b_liver.sum()
#print 'Total absorbed dose', dose_target*1.09993e15
#print 'Beta minus aborbed dose', doseBetaM*1.09993e15
print >> outFile, 'Liver volume', 0.976562 * 0.976562 * 5 * b_liver.sum()/1000
print >> outFile, 'Liver mass', 1.0616 * 0.976562 * 0.976562 * 5 * b_liver.sum()/1000 
outFile.close()
