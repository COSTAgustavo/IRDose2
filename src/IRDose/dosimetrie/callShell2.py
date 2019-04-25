import subprocess
organes = ['Liver']  #, 'Kidneys', 'Spleen']
for organeIt in organes:
   print '\n \t***********************************' 
   print ' \t************** ', organeIt, ' **************' 
   print ' \t***********************************\n'

   subprocess.call('./patientDose_multi.sh ' + organeIt, shell=True)

   #print '\n ----------------- gamma --------------'
   #subprocess.call('./docker_multi.sh G', shell=True)

   #print '\n ----------------- X ----------------- '
   #subprocess.call('./docker_multi.sh X', shell=True)

   #print '\n ----------------- IE ----------------- '
   #subprocess.call('./docker_multi.sh IE', shell=True)

   #print '\n ----------------- AE ----------------- '
   #subprocess.call('./docker_multi.sh AE', shell=True)

   #print '\n ----------------- Beta minus ----------------- '
   #subprocess.call('./docker_multi.sh betaMinus', shell=True)

print 'Le Fin'
