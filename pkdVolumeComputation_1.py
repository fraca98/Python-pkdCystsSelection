import itk
import os
import sys
import numpy
numpy.set_printoptions(threshold=sys.maxsize) #show entire array in numpy

path=input("Enter the path: T2_labeled_ok.mha")

Dim=3
LabelPixelType=itk.US
LabeledImageType=itk.Image[LabelPixelType,Dim]

LabelReaderType=itk.ImageFileReader[LabeledImageType]
labelReader=LabelReaderType.New()
labelReader.SetFileName(path)

try:
    labelReader.Update()
except Exception as error:
    print(error)
    sys.exit(1)

labeledImage=labelReader.GetOutput()
spacing=labeledImage.GetSpacing()

voxelVolume=spacing[0]*spacing[1]*spacing[2]

array=itk.GetArrayViewFromImage(labeledImage)
numberOfCystVoxels=0
print("Processing pixels")
for z in array:
    for y in z:
        for x in y:
                if(x!=0):
                    numberOfCystVoxels=numberOfCystVoxels+1

cystVolume=numberOfCystVoxels*voxelVolume
print("Volume: ",round(cystVolume,3)," mm^3")
print("Volume: ",round(cystVolume/1000,3)," ml")

