import vtk
import numpy
import PIL
import subprocess as sp
import sys

userName = sys.argv[1]
CTpatient = sys.argv[2]
argName = CTpatient[9:len(CTpatient)-4]
#PathDicom = "media/"+argName

sp.Popen(['mkdir', '-p', CTpatient[3:len(CTpatient)-4]])
sp.call('unzip ' +CTpatient[3:]+' -d '+CTpatient[3:len(CTpatient)-4], shell=True)

readerImg = vtk.vtkDICOMImageReader()
#readerImg.SetDirectoryName(PathDicom)
readerImg.SetDirectoryName(CTpatient[3:len(CTpatient)-4])
readerImg.Update()

imageWriter = vtk.vtkMetaImageWriter()
imageWriter.SetCompression(False)
imageWriter.SetFileName("dosimetrie/stdGATE/data/"+userName+".mhd")
#imageWriter.SetFileName(CTpatient[9:len(CTpatient)-4]+".mhd")
imageWriter.SetInputData(readerImg.GetOutput())
imageWriter.Write()

sp.call('rm -r ' +CTpatient[3:len(CTpatient)-4]+ ' media/__*', shell=True)
sp.call('rm -r '+CTpatient[3:], shell=True)

with open("dosimetrie/stdGATE/data/"+userName+'.mhd') as file:
   for  line in file:
     if line.startswith('DimSize'):
        dim_x = line.split()[2]
        dim_y = line.split()[3]
        dim_z = line.split()[4]
     if line.startswith('ElementSpacing'):
        pixelSize_x = line.split()[2]
        pixelSize_y = line.split()[3]
        pixelSize_z = line.split()[4]

print('Dimensions', dim_x, dim_y, dim_z)
print('Element Spacing', pixelSize_x, pixelSize_y, pixelSize_z)

shift_x = (float(dim_x)*float(pixelSize_x))/2
shift_y = (float(dim_y)*float(pixelSize_y))/2
shift_z = (float(dim_z)*float(pixelSize_z))/2

print('Shifts:', shift_x, shift_y, shift_z)

#subprocess.call('python DICOM_to_mhd_source.py' +argName + 'target_1' + 'target1' + 'target_2' + 'target2', shell=True)
sp.call('bash dosimetrie/patientDose_multi.sh ' + userName + ' ' + str(dim_x) + ' ' + str(dim_y) + ' ' + str(dim_z) + ' ' + str(shift_x) + ' ' + str(shift_y) + ' ' + str(shift_z) + ' ' + str(pixelSize_x) + ' ' + str(pixelSize_y) + ' ' + str(pixelSize_z), shell=True)
