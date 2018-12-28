
# coding: utf-8

# # Connect and create a metadata to the database ICRP and GATE

# In[1]:

import sqlalchemy

def connect(user, password, db, host='localhost', port=5432):
    '''Returns a connection and a metadata object'''
    # We connect with the help of the PostgreSQL URL
    # postgresql://postgres:postgres@localhost:5432/gate_v7_2
    url = 'postgresql://{}:{}@{}:{}/{}'
    url = url.format(user, password, host, port, db)

    # The return value of create_engine() is our connection object
    con = sqlalchemy.create_engine(url, client_encoding='utf8')

    # We then bind the connection to MetaData()
    meta = sqlalchemy.MetaData(bind=con) #, reflect=True)
    meta.reflect()

    return con, meta


# In[2]:

con_icrp110_v1_2, meta_icrp110_v1_2 = connect('postgres', 'postgres', 'icrp110_v1_2')
print con_icrp110_v1_2
print meta_icrp110_v1_2


# In[3]:

con_gate_v7_2, meta_gate_v7_2 = connect('postgres', 'postgres', 'gate_v7_2')
print con_gate_v7_2
print meta_gate_v7_2


# # Read results from the database

# In[18]:

import pandas as pd
import numpy as np

# should be the directory where the results are stored on the database server
#rootdir = '/database/results/gate7.2/'
rootdir = '/home/pogo/OpenDose/'

# read the gate database
gp = pd.read_sql('params', con_gate_v7_2)
gf = pd.read_sql('files', con_gate_v7_2)

# get the database runID from parameters
Model = "ICRP110_v1_2_AF"
Particle = "electrons"
#Particle = "photons"
OrganID = 95
Energy_MeV = 0.05
NbEvents = 100000000.0
RunID = gp[(gp['Model']==Model) & (gp['Particle']==Particle) & (gp['OrganID']==OrganID) & 
           (gp['Energy_MeV']==Energy_MeV) & (gp['NbEvents']==NbEvents)].RunID.values[0]

# or select a RunID
#RunID = 0

# get database entry from the RunID
gate_params_run = gp[gp['RunID'] == RunID]
gate_files_run = gf[gf['RunID'] == RunID]

# get parameters for a RunID
#model = gate_params_run['Model'].values[0]
#particle = gate_params_run['Particle'].values[0]
#organID = gate_params_run['OrganID'].values[0]
#energy = gate_params_run['Energy_MeV'].values[0]
#nb_events = gate_params_run['NbEvents'].values[0]

# get filenames for this RunID
file_Dose = rootdir + gate_files_run['File_Dose'].values[0]
file_Dose2 = rootdir + gate_files_run['File_Dose-Squared'].values[0]
file_DoseSigma = rootdir + gate_files_run['File_Dose-Uncertainty'].values[0]

# get corresponding ICRP data in the icrp database
if 'AF' in Model:
    icrp_files = pd.read_sql('AF_files', con_icrp110_v1_2)
    icrp_organs = pd.read_sql('AF_organs', con_icrp110_v1_2)
elif 'AM' in Model:
    icrp_files = pd.read_sql('AM_files', con_icrp110_v1_2)
    icrp_organs = pd.read_sql('AM_organs', con_icrp110_v1_2)
file_image = rootdir + icrp_files['File_image-mhd'].values[0]
image = np.fromfile(file_image.replace('mhd','raw'), dtype=np.int16)
organ_name = icrp_organs[icrp_organs['Organ_ID'] == OrganID]['Organ_name'].values[0]

# read mhd parameters
mhd_param = pd.read_table(file_Dose,header=None,sep=' = ',index_col=0,engine='python')
voxel_size = map(float, mhd_param.loc[['ElementSpacing']].values[0][0].split())
voxel_volume = voxel_size[0]*voxel_size[1]*voxel_size[2]/1000
dim_size = map(int, mhd_param.loc[['DimSize']].values[0][0].split())
nb_voxels = dim_size[0]*dim_size[1]*dim_size[2]

# get mean Dose 3D image (Dose is in Gy (J/kg))
Dose = np.fromfile(file_Dose.replace('mhd','raw'), dtype=np.float32)
Dose = Dose/NbEvents
# get dose squared sums 3D image
Dose2 = np.fromfile(file_Dose2.replace('mhd','raw'), dtype=np.float32)
Dose2 = Dose2/NbEvents
# get corresponding relative statistical uncertainty
DoseSigma = np.fromfile(file_DoseSigma.replace('mhd','raw'), dtype=np.float32)
# get absolute statistical uncertainties
DoseSigma_abs = DoseSigma * Dose

print gate_params_run
print "Number of voxels in image:", nb_voxels
print "Size of voxels:", voxel_size, 'mm'
print 'Volume of a voxel:', voxel_volume, 'cm3'
if (len(Dose)+len(Dose2)+len(DoseSigma) != 3*nb_voxels):
    print "Reading binary type incorrect"
else:
    print "Reading binary images ok!"


# # Process SAFs from data

# In[19]:

MeV = 1.602176565e-13 # MeV in Joules
# energy emitted from the source in Joules per event
E_source = Energy_MeV*MeV

TargetID = 95

# get target name and density
target_name = icrp_organs[icrp_organs['Organ_ID'] == TargetID]['Organ_name'].values[0]
target_density = icrp_organs[icrp_organs['Organ_ID'] == TargetID]['Tissue_density'].values[0]

# make boolean mask of source from image
b_source = (image == OrganID)

# make boolean mask of target from image
b_target = (image == TargetID)

# volume of target
target_volume = voxel_volume*b_target.sum()

# average dose per event per voxel in the target
dose_target = Dose[b_target].sum()/b_target.sum()
# SAF
SAF = dose_target/E_source
# uncertainty of the dose in target, quadratic sum
dose_target_SigmaQ = np.sqrt((DoseSigma_abs[b_target]**2).sum())/b_target.sum()
# uncertainty of the dose in target, eq. 2 Chetty et al.
dose_target_Sigma = np.sqrt(1/(NbEvents*b_target.sum()-1)*(Dose2[b_target].sum()/b_target.sum()-(Dose[b_target].sum()/b_target.sum())**2))
# SAF relative statistical uncertainty
SAF_SigmaQ = dose_target_SigmaQ/dose_target*100
SAF_Sigma = dose_target_Sigma/dose_target*100

print 'Number of voxel in source', organ_name, '( ID', OrganID, ') :', b_source.sum()
print 'Number of voxel in target', target_name, '( ID', TargetID, ') :', b_target.sum()
print 'Target tissue density:', target_density, 'g.cm-3'
print 'SAF for', Energy_MeV, 'MeV', Particle, ':'
print organ_name, '->', target_name, ':', SAF, 'kg-1 +/-', SAF_Sigma, '%'
print organ_name, '->', target_name, ':', SAF*target_density*target_volume/1000, '+/-', SAF_SigmaQ, '%'


# In[55]:

f_organVoxels = open('organ_NbVoxels.txt','w')

print 'SAFs for', Energy_MeV, 'MeV', Particle, ':'
for TargetID in range(1,141):
    # get target name and density
    target_name = icrp_organs[icrp_organs['Organ_ID'] == TargetID]['Organ_name'].values[0]
    target_density = icrp_organs[icrp_organs['Organ_ID'] == TargetID]['Tissue_density'].values[0]
    # make boolean mask of target
    b_target = (image == TargetID)
    # volume of target
    f_organVoxels.write(str(b_target.sum())+'\t')
    target_volume = voxel_volume*b_target.sum()
    # average dose per event per voxel in the target
    dose_target = Dose[b_target].sum()/b_target.sum()
    # SAF
    SAF = dose_target/E_source
    # uncertainty of the dose in target, quadratic sum
    dose_target_SigmaQ = np.sqrt((DoseSigma_abs[b_target]**2).sum())/b_target.sum()
    # uncertainty of the dose in target, eq. 2 Chetty et al.
    dose_target_Sigma = np.sqrt(1/(NbEvents*b_target.sum()-1)*(Dose2[b_target].sum()/b_target.sum()-(Dose[b_target].sum()/b_target.sum())**2))
    # SAF relative statistical uncertainty
    SAF_SigmaQ = dose_target_SigmaQ/dose_target*100
    SAF_Sigma = dose_target_Sigma/dose_target*100
    # Insert SAF in the database
    #SAF_list = {'RunID':[RunID], 'TargetID':[TargetID], 'SAF':[SAF], 'SAF-uncertainty':[SAF_SigmaQ]}
    SAF_list = {'RunID':[RunID], 'TargetID':[TargetID], 'SAF':[SAF], 'SAF-uncertainty':[SAF_Sigma], 'SAF-uncertainty_Q':[SAF_SigmaQ]}
    SAF_table =  pd.DataFrame(SAF_list)
    filename_out = 'SourceID'+str(OrganID)+'E'+str(Energy_MeV)+'MeV.txt'
    SAF_table.to_csv(filename_out, header=None, index=None, sep=' ', na_rep='NaN', mode='a')
    #SAF_table.to_sql('SAFs', con_gate_v7_2, if_exists='append', index=False)
    print organ_name, '->', target_name, ':', SAF, 'kg-1 +/-', SAF_Sigma, '%, +/-', SAF_SigmaQ, '%'
    #print organ_name, '->', target_name, ':', SAF*target_density*target_volume/1000, '+/-', SAF_SigmaQ, '%'
    #print organ_name, '->', target_name, ':', SAF*target_density*target_volume/1000, '+/-', SAF_Sigma, '%'
    #print 'sigma relative difference between methods:', SAF_Sigma/SAF_SigmaQ

f_organVoxels.close()


# In[ ]:




# # Process SAFs from data: OrganID -> all targets

# In[101]:

import pandas as pd
import numpy as np

MeV = 1.602176565e-13 # MeV in Joules
Model = "ICRP110_v1_2_AF"

# should be the directory where the results are stored on the database server
#rootdir = '/database/results/gate7.2/'
rootdir = '/home/pogo/OpenDose/'

# get ICRP data in the icrp database
if 'AF' in Model:
    icrp_files = pd.read_sql('AF_files', con_icrp110_v1_2)
    icrp_organs = pd.read_sql('AF_organs', con_icrp110_v1_2)
elif 'AM' in Model:
    icrp_files = pd.read_sql('AM_files', con_icrp110_v1_2)
    icrp_organs = pd.read_sql('AM_organs', con_icrp110_v1_2)
file_image = rootdir + icrp_files['File_image-mhd'].values[0]
image = np.fromfile(file_image.replace('mhd','raw'), dtype=np.int16)

# read the gate database
gp = pd.read_sql('params', con_gate_v7_2)
gf = pd.read_sql('files', con_gate_v7_2)

# get the database runID from parameters
Particle = "electrons"
#Particle = "photons"
OrganID = 95
NbEvents = 100000000.0

f_SAF = open('SAF_SourceID'+str(OrganID)+'_'+Particle+'.txt','w')
f_SAF_Sigma = open('SAF_Sigma_SourceID'+str(OrganID)+'_'+Particle+'.txt','w')
f_SAF_SigmaQ = open('SAF_SigmaQ_SourceID'+str(OrganID)+'_'+Particle+'.txt','w')

with open('energies.dat', 'r') as f:
    for line in f:
        for s in line.split(' '):
            Energy_MeV = float(s)
            RunID = gp[(gp['Model']==Model) & (gp['Particle']==Particle) & (gp['OrganID']==OrganID) & 
                       (gp['Energy_MeV']==Energy_MeV) & (gp['NbEvents']==NbEvents)].RunID.values[0]
            # get database entry from the RunID
            gate_params_run = gp[gp['RunID'] == RunID]
            gate_files_run = gf[gf['RunID'] == RunID]
            # get filenames for this RunID
            file_Dose = rootdir + gate_files_run['File_Dose'].values[0]
            file_Dose2 = rootdir + gate_files_run['File_Dose-Squared'].values[0]
            file_DoseSigma = rootdir + gate_files_run['File_Dose-Uncertainty'].values[0]
            # get mean Dose 3D image (Dose is in Gy (J/kg))
            Dose = np.fromfile(file_Dose.replace('mhd','raw'), dtype=np.float32)
            Dose = Dose/NbEvents
            # get dose squared sums 3D image
            Dose2 = np.fromfile(file_Dose2.replace('mhd','raw'), dtype=np.float32)
            Dose2 = Dose2/NbEvents
            # get corresponding relative statistical uncertainty
            DoseSigma = np.fromfile(file_DoseSigma.replace('mhd','raw'), dtype=np.float32)
            # get absolute statistical uncertainties
            DoseSigma_abs = DoseSigma * Dose
            # energy emitted from the source in Joules per event
            E_source = Energy_MeV*MeV

            SAF_list = [Energy_MeV]
            SAF_Sigma_list = [Energy_MeV]
            SAF_SigmaQ_list = [Energy_MeV]

            for TargetID in range(1,141):
                # make boolean mask of target
                b_target = (image == TargetID)
                # average dose per event per voxel in the target
                dose_target = Dose[b_target].sum()/b_target.sum()
                # SAF
                SAF = dose_target/E_source
                # uncertainty of the dose in target, quadratic sum
                dose_target_SigmaQ = np.sqrt((DoseSigma_abs[b_target]**2).sum())/b_target.sum()
                # uncertainty of the dose in target, eq. 2 Chetty et al.
                dose_target_Sigma = np.sqrt(1/(NbEvents*b_target.sum()-1)*(Dose2[b_target].sum()/b_target.sum()-(Dose[b_target].sum()/b_target.sum())**2))
                # SAF statistical uncertainty
                SAF_SigmaQ = dose_target_SigmaQ/E_source
                SAF_Sigma = dose_target_Sigma/E_source
                # SAF relative statistical uncertainty
                #SAF_SigmaQ = dose_target_SigmaQ/dose_target*100
                #SAF_Sigma = dose_target_Sigma/dose_target*100
                # append result to SAF lists
                SAF_list.append(SAF)
                SAF_Sigma_list.append(SAF_Sigma)
                SAF_SigmaQ_list.append(SAF_SigmaQ)

            f_SAF.writelines( '\t'.join(map(repr, SAF_list))+'\n' )
            f_SAF_Sigma.writelines( '\t'.join(map(repr, SAF_Sigma_list))+'\n' )
            f_SAF_SigmaQ.writelines( '\t'.join(map(repr, SAF_SigmaQ_list))+'\n' )

f_SAF.close()
f_SAF_Sigma.close()
f_SAF_SigmaQ.close()


# # Process SAFs from data: OrganID -> sum of targets

# In[207]:

import pandas as pd
import numpy as np

MeV = 1.602176565e-13 # MeV in Joules
Model = "ICRP110_v1_2_AF"

# should be the directory where the results are stored on the database server
#rootdir = '/database/results/gate7.2/'
rootdir = '/home/pogo/OpenDose/'

# get ICRP data in the icrp database
if 'AF' in Model:
    icrp_files = pd.read_sql('AF_files', con_icrp110_v1_2)
    icrp_organs = pd.read_sql('AF_organs', con_icrp110_v1_2)
elif 'AM' in Model:
    icrp_files = pd.read_sql('AM_files', con_icrp110_v1_2)
    icrp_organs = pd.read_sql('AM_organs', con_icrp110_v1_2)
file_image = rootdir + icrp_files['File_image-mhd'].values[0]
image = np.fromfile(file_image.replace('mhd','raw'), dtype=np.int16)

# read the gate database
gp = pd.read_sql('params', con_gate_v7_2)
gf = pd.read_sql('files', con_gate_v7_2)

# get the database runID from parameters
#Particle = "electrons"
Particle = "photons"
OrganID = 95
NbEvents = 100000000.0
#TargetIDs = [62,63,64,65] # breasts
TargetIDs = [72] # stomach wall
#TargetIDs = [76,78,80,82,84] # colon
#TargetIDs = [95] # liver
#TargetIDs = [97,99] # lungs

f_SAF = open('SAF_SourceID'+str(OrganID)+'_TargetID'+str(TargetIDs).replace(' ','')+'_'+Particle+'.txt','w')
f_SAF_Sigma = open('SAF_Sigma_SourceID'+str(OrganID)+'_TargetID'+str(TargetIDs).replace(' ','').replace(' ','')+'_'+Particle+'.txt','w')
f_SAF_SigmaQ = open('SAF_SigmaQ_SourceID'+str(OrganID)+'_TargetID'+str(TargetIDs).replace(' ','')+'_'+Particle+'.txt','w')

with open('energies_7.dat', 'r') as f:
    for line in f:
        for s in line.split(' '):
            Energy_MeV = float(s)
            RunID = gp[(gp['Model']==Model) & (gp['Particle']==Particle) & (gp['OrganID']==OrganID) & 
                       (gp['Energy_MeV']==Energy_MeV) & (gp['NbEvents']==NbEvents)].RunID.values[0]
            # get database entry from the RunID
            gate_params_run = gp[gp['RunID'] == RunID]
            gate_files_run = gf[gf['RunID'] == RunID]
            # get filenames for this RunID
            file_Dose = rootdir + gate_files_run['File_Dose'].values[0]
            file_Dose2 = rootdir + gate_files_run['File_Dose-Squared'].values[0]
            file_DoseSigma = rootdir + gate_files_run['File_Dose-Uncertainty'].values[0]
            # get mean Dose 3D image (Dose is in Gy (J/kg))
            Dose = np.fromfile(file_Dose.replace('mhd','raw'), dtype=np.float32)
            Dose = Dose/NbEvents
            # get dose squared sums 3D image
            Dose2 = np.fromfile(file_Dose2.replace('mhd','raw'), dtype=np.float32)
            Dose2 = Dose2/NbEvents
            # get corresponding relative statistical uncertainty
            DoseSigma = np.fromfile(file_DoseSigma.replace('mhd','raw'), dtype=np.float32)
            # get absolute statistical uncertainties
            DoseSigma_abs = DoseSigma * Dose
            # energy emitted from the source in Joules per event
            E_source = Energy_MeV*MeV

            SAF_list = [Energy_MeV]
            SAF_Sigma_list = [Energy_MeV]
            SAF_SigmaQ_list = [Energy_MeV]

            image_temp = image
            for TargetID in TargetIDs:
                image_temp[image_temp == TargetID] = -100
            # make boolean mask of target
            b_target = (image_temp == -100)
            # average dose per event per voxel in the target
            dose_target = Dose[b_target].sum()/b_target.sum()
            # SAF
            SAF = dose_target/E_source
            # uncertainty of the dose in target, quadratic sum
            dose_target_SigmaQ = np.sqrt((DoseSigma_abs[b_target]**2).sum())/b_target.sum()
            # uncertainty of the dose in target, eq. 2 Chetty et al.
            dose_target_Sigma = np.sqrt(1/(NbEvents*b_target.sum()-1)*(Dose2[b_target].sum()/b_target.sum()-(Dose[b_target].sum()/b_target.sum())**2))
            # SAF statistical uncertainty
            SAF_SigmaQ = dose_target_SigmaQ/E_source
            SAF_Sigma = dose_target_Sigma/E_source
            # SAF relative statistical uncertainty
            #SAF_SigmaQ = dose_target_SigmaQ/dose_target*100
            #SAF_Sigma = dose_target_Sigma/dose_target*100
            # append result to SAF lists
            SAF_list.append(SAF)
            SAF_Sigma_list.append(SAF_Sigma)
            SAF_SigmaQ_list.append(SAF_SigmaQ)

            f_SAF.writelines( '\t'.join(map(repr, SAF_list))+'\n' )
            f_SAF_Sigma.writelines( '\t'.join(map(repr, SAF_Sigma_list))+'\n' )
            f_SAF_SigmaQ.writelines( '\t'.join(map(repr, SAF_SigmaQ_list))+'\n' )

f_SAF.close()
f_SAF_Sigma.close()
f_SAF_SigmaQ.close()


# In[295]:

import matplotlib.pyplot as plt
import numpy as np
get_ipython().magic(u'matplotlib inline')

Particle = "electrons"
OrganID = 95
TargetID = 95

SAF_data = np.loadtxt('data/SAF_SourceID'+str(OrganID)+'_'+Particle+'.txt')
SAF_Sigma_data = np.loadtxt('data/SAF_Sigma_SourceID'+str(OrganID)+'_'+Particle+'.txt')
GATErin_SAF_data = np.loadtxt('data/GATErin_SAF_SourceID'+str(OrganID)+'_'+Particle+'.txt',skiprows=1)
GATErin_SAF_Sigma_data = np.loadtxt('data/GATErin_SAF_Sigma_SourceID'+str(OrganID)+'_'+Particle+'.txt',skiprows=1)
MCNPX_SAF_data = np.loadtxt('data/MCNPX_SAF_SourceID'+str(OrganID)+'_'+Particle+'.txt',skiprows=1)
EGSnrc_SAF_data = np.loadtxt('data/EGSnrc_SAF_SourceID'+str(OrganID)+'_'+Particle+'.txt',skiprows=1)

#print SAF_data[:,0]
#print SAF_data[:,TargetID]
#print SAF_Sigma_data[:,TargetID]

plt.figure()
plt.title('Liver -> Liver')
plt.xscale('log')
plt.yscale('log')
plt.xlim([0.005,10])
plt.xlabel('Energy (MeV)')
plt.ylabel('SAF ($kg^{-1}$)')
plt.errorbar(SAF_data[:,0],SAF_data[:,TargetID],yerr=SAF_Sigma_data[:,TargetID], label='GATE 7.2')
plt.plot(GATErin_SAF_data[:,0],GATErin_SAF_data[:,5], linestyle='None',marker='+', label='GATErin')
plt.legend(numpoints=1,loc=0)


# In[297]:

TargetID = 72

plt.figure()
plt.title('Liver -> Stomach wall')
plt.xscale('log')
plt.yscale('log')
plt.xlim([0.005,10])
plt.xlabel('Energy (MeV)')
plt.ylabel('SAF ($kg^{-1}$)')
plt.errorbar(SAF_data[:,0],SAF_data[:,TargetID],yerr=SAF_Sigma_data[:,TargetID],label='GATE 7.2')
#plt.errorbar(GATErin_SAF_data[:,0],GATErin_SAF_data[:,4],yerr=GATErin_SAF_Sigma_data[:,4])
plt.plot(MCNPX_SAF_data[:,0],MCNPX_SAF_data[:,4], linestyle='None',marker='x',markersize=10,label='ICRP_MCNPX')
plt.plot(EGSnrc_SAF_data[:,0],EGSnrc_SAF_data[:,4], linestyle='None',marker='x',markersize=7,label='ICRP_EGSnrc')
plt.legend(numpoints=1,loc=4)


# In[255]:

TargetIDs = [62,63,64,65] # breasts

SAF_data = np.loadtxt('data/SAF_SourceID'+str(OrganID)+'_TargetID'+str(TargetIDs).replace(' ','')+'_'+Particle+'.txt')
SAF_Sigma_data = np.loadtxt('data/SAF_Sigma_SourceID'+str(OrganID)+'_TargetID'+str(TargetIDs).replace(' ','')+'_'+Particle+'.txt')

plt.figure()
plt.title('Liver -> ')
plt.xscale('log')
plt.yscale('log')
plt.xlim([0.005,10])
plt.xlabel('Energy (MeV)')
plt.ylabel('SAF ($kg^{-1}$)')
plt.errorbar(SAF_data[:,0],SAF_data[:,1],yerr=SAF_Sigma_data[:,1])
plt.errorbar(GATErin_SAF_data[:,0],GATErin_SAF_data[:,1],yerr=GATErin_SAF_Sigma_data[:,1])
plt.plot(MCNPX_SAF_data[:,0],MCNPX_SAF_data[:,1])
plt.plot(EGSnrc_SAF_data[:,0],EGSnrc_SAF_data[:,1])


# In[183]:

TargetIDs = [76,78,80,82,84] # colon

SAF_data = np.loadtxt('data/SAF_SourceID'+str(OrganID)+'_TargetID'+str(TargetIDs).replace(' ','')+'_'+Particle+'.txt')
SAF_Sigma_data = np.loadtxt('data/SAF_Sigma_SourceID'+str(OrganID)+'_TargetID'+str(TargetIDs).replace(' ','')+'_'+Particle+'.txt')

plt.figure()
plt.title('Liver -> ')
plt.xscale('log')
plt.yscale('log')
plt.xlim([0.005,10])
plt.xlabel('Energy (MeV)')
plt.ylabel('SAF ($kg^{-1}$)')
plt.errorbar(SAF_data[:,0],SAF_data[:,1],yerr=SAF_Sigma_data[:,1])
plt.errorbar(GATErin_SAF_data[:,0],GATErin_SAF_data[:,2],yerr=GATErin_SAF_Sigma_data[:,2])
plt.plot(MCNPX_SAF_data[:,0],MCNPX_SAF_data[:,2])
plt.plot(EGSnrc_SAF_data[:,0],EGSnrc_SAF_data[:,2])


# In[182]:

TargetIDs = [97,99] # lungs

SAF_data = np.loadtxt('data/SAF_SourceID'+str(OrganID)+'_TargetID'+str(TargetIDs).replace(' ','')+'_'+Particle+'.txt')
SAF_Sigma_data = np.loadtxt('data/SAF_Sigma_SourceID'+str(OrganID)+'_TargetID'+str(TargetIDs).replace(' ','')+'_'+Particle+'.txt')

plt.figure()
plt.title('Liver -> ')
plt.xscale('log')
plt.yscale('log')
plt.xlim([0.005,10])
plt.xlabel('Energy (MeV)')
plt.ylabel('SAF ($kg^{-1}$)')
plt.errorbar(SAF_data[:,0],SAF_data[:,1],yerr=SAF_Sigma_data[:,1])
plt.errorbar(GATErin_SAF_data[:,0],GATErin_SAF_data[:,3],yerr=GATErin_SAF_Sigma_data[:,3])
plt.plot(MCNPX_SAF_data[:,0],MCNPX_SAF_data[:,3])
plt.plot(EGSnrc_SAF_data[:,0],EGSnrc_SAF_data[:,3])


# In[300]:

import matplotlib.pyplot as plt
import numpy as np

Particle = "photons"
OrganID = 95
TargetID = 95

SAF_data = np.loadtxt('data/SAF_SourceID'+str(OrganID)+'_'+Particle+'.txt')
SAF_Sigma_data = np.loadtxt('data/SAF_Sigma_SourceID'+str(OrganID)+'_'+Particle+'.txt')
GATErin_SAF_data = np.loadtxt('data/GATErin_SAF_SourceID'+str(OrganID)+'_'+Particle+'.txt',skiprows=1)
GATErin_SAF_Sigma_data = np.loadtxt('data/GATErin_SAF_Sigma_SourceID'+str(OrganID)+'_'+Particle+'.txt',skiprows=1)
MCNPX_SAF_data = np.loadtxt('data/MCNPX_SAF_SourceID'+str(OrganID)+'_'+Particle+'.txt',skiprows=1)
EGSnrc_SAF_data = np.loadtxt('data/EGSnrc_SAF_SourceID'+str(OrganID)+'_'+Particle+'.txt',skiprows=1)

#print SAF_data[:,0]
#print SAF_data[:,TargetID]
#print SAF_Sigma_data[:,TargetID]

plt.figure()
plt.title('Liver -> ')
plt.xscale('log')
plt.yscale('log')
plt.xlim([0.005,10])
plt.xlabel('Energy (MeV)')
plt.ylabel('SAF ($kg^{-1}$)')
plt.errorbar(SAF_data[:,0],SAF_data[:,TargetID],yerr=SAF_Sigma_data[:,TargetID])
plt.plot(GATErin_SAF_data[:,0],GATErin_SAF_data[:,5])


# In[302]:

TargetID = 72

plt.figure()
plt.title('Liver -> Stomach wall')
plt.xscale('log')
plt.yscale('log')
plt.xlim([0.005,10])
plt.xlabel('Energy (MeV)')
plt.ylabel('SAF ($kg^{-1}$)')
plt.errorbar(SAF_data[:,0],SAF_data[:,TargetID],yerr=SAF_Sigma_data[:,TargetID],label='GATE 7.2')
#plt.errorbar(GATErin_SAF_data[:,0],GATErin_SAF_data[:,4],yerr=GATErin_SAF_Sigma_data[:,4])
plt.plot(MCNPX_SAF_data[:,0],MCNPX_SAF_data[:,4], linestyle='None',marker='x',markersize=10,label='ICRP_MCNPX')
plt.plot(EGSnrc_SAF_data[:,0],EGSnrc_SAF_data[:,4], linestyle='None',marker='x',markersize=7,label='ICRP_EGSnrc')
plt.legend(numpoints=1,loc=0)


# In[189]:

TargetIDs = [62,63,64,65] # breasts

SAF_data = np.loadtxt('data/SAF_SourceID'+str(OrganID)+'_TargetID'+str(TargetIDs).replace(' ','')+'_'+Particle+'.txt')
SAF_Sigma_data = np.loadtxt('data/SAF_Sigma_SourceID'+str(OrganID)+'_TargetID'+str(TargetIDs).replace(' ','')+'_'+Particle+'.txt')

plt.figure()
plt.title('Liver -> ')
plt.xscale('log')
plt.yscale('log')
plt.xlim([0.005,10])
plt.xlabel('Energy (MeV)')
plt.ylabel('SAF ($kg^{-1}$)')
plt.errorbar(SAF_data[:,0],SAF_data[:,1],yerr=SAF_Sigma_data[:,1])
plt.errorbar(GATErin_SAF_data[:,0],GATErin_SAF_data[:,1],yerr=GATErin_SAF_Sigma_data[:,1])
plt.plot(MCNPX_SAF_data[:,0],MCNPX_SAF_data[:,1])
plt.plot(EGSnrc_SAF_data[:,0],EGSnrc_SAF_data[:,1])


# In[190]:

TargetIDs = [76,78,80,82,84] # colon

SAF_data = np.loadtxt('data/SAF_SourceID'+str(OrganID)+'_TargetID'+str(TargetIDs).replace(' ','')+'_'+Particle+'.txt')
SAF_Sigma_data = np.loadtxt('data/SAF_Sigma_SourceID'+str(OrganID)+'_TargetID'+str(TargetIDs).replace(' ','')+'_'+Particle+'.txt')

plt.figure()
plt.title('Liver -> ')
plt.xscale('log')
plt.yscale('log')
plt.xlim([0.005,10])
plt.xlabel('Energy (MeV)')
plt.ylabel('SAF ($kg^{-1}$)')
plt.errorbar(SAF_data[:,0],SAF_data[:,1],yerr=SAF_Sigma_data[:,1])
plt.errorbar(GATErin_SAF_data[:,0],GATErin_SAF_data[:,2],yerr=GATErin_SAF_Sigma_data[:,2])
plt.plot(MCNPX_SAF_data[:,0],MCNPX_SAF_data[:,2])
plt.plot(EGSnrc_SAF_data[:,0],EGSnrc_SAF_data[:,2])


# In[191]:

TargetIDs = [97,99] # lungs

SAF_data = np.loadtxt('data/SAF_SourceID'+str(OrganID)+'_TargetID'+str(TargetIDs).replace(' ','')+'_'+Particle+'.txt')
SAF_Sigma_data = np.loadtxt('data/SAF_Sigma_SourceID'+str(OrganID)+'_TargetID'+str(TargetIDs).replace(' ','')+'_'+Particle+'.txt')

plt.figure()
plt.title('Liver -> ')
plt.xscale('log')
plt.yscale('log')
plt.xlim([0.005,10])
plt.xlabel('Energy (MeV)')
plt.ylabel('SAF ($kg^{-1}$)')
plt.errorbar(SAF_data[:,0],SAF_data[:,1],yerr=SAF_Sigma_data[:,1])
plt.errorbar(GATErin_SAF_data[:,0],GATErin_SAF_data[:,3],yerr=GATErin_SAF_Sigma_data[:,3])
plt.plot(MCNPX_SAF_data[:,0],MCNPX_SAF_data[:,3])
plt.plot(EGSnrc_SAF_data[:,0],EGSnrc_SAF_data[:,3])

