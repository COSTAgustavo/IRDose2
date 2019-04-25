#####                                                    |   True or False  | file paths when True
##### usage --> python DICOM_to_mhd_source argName source target_1 target_2 target1 target2
#####

import numpy
import PIL
import subprocess as sp
import sys
import vtk

userName = sys.argv[1]
list = ['source', 'target_1', 'target_2']
for organs in list:
    print(organs)
    if organs == 'source': 
         organPath = sys.argv[2]
    if organs == 'target_1':
        if sys.argv[3] == 'False':
           break
        else:
           organPath = sys.argv[5]
    if organs == 'target_2':
        if sys.argv[4] == 'False':
           break
        else:
           organPath = sys.argv[6]
    PathDicom = organPath[3:]
    print(PathDicom)

    sp.Popen(['mkdir', '-p', PathDicom[:len(PathDicom)-4]])
    sp.call('unzip '+PathDicom+' -d' + PathDicom[:len(PathDicom)-4], shell=True)
    sp.call('rm -r '+PathDicom+' media/__*', shell=True)


    readerImg = vtk.vtkDICOMImageReader()
    readerImg.SetDirectoryName(PathDicom[:len(PathDicom)-4])
    readerImg.Update()

    dims = readerImg.GetOutput().GetDimensions()
    print(dims)
    print("Progression...")

    Conversion=vtk.vtkImageData()
    Conversion.DeepCopy(readerImg.GetOutput())
    for z in range(dims[2]):
      	for y in range(dims[1]):
           for x in range(dims[0]):
               a=Conversion.GetScalarComponentAsFloat(x, y, z, 0)
               if a !=0:
                   a=1
                   Conversion.SetScalarComponentFromFloat(x, y, z, 0, a)
    Conversion.Modified()

    caca=[0,0]
    Conversion.GetScalarRange(caca)
    print(caca)

    imageWriter = vtk.vtkMetaImageWriter()
    imageWriter.SetCompression(False)
    print("dosimetrie/stdGATE/data/"+userName+PathDicom[6:len(PathDicom)-4]+".mhd")
    #print(organs)
    imageWriter.SetFileName("dosimetrie/stdGATE/data/"+userName+'_'+organs+".mhd")
    imageWriter.SetInputData(Conversion)
    print('Wrinting mhd image')
    imageWriter.Write()

    sp.call('rm -r ' +PathDicom[:len(PathDicom)-4]+ ' media/__*', shell=True)
