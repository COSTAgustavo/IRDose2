import subprocess

print('Converting DICOM to mhd.')
subprocess.call('python DICOM_to_mhd.py' + argName + target_1 + target_2, shell=True)

print('Lauching simulation.')
subprocess.call('bash dosimetrie/patientDose_multi.sh ' + argName , shell=True)  

print('Calculationg absorbed dose.')
subprocess.call('python dosimetrie/doseToOrgans.py' + argName + target_1 + target_2, shell=True)  

print('Done !')

