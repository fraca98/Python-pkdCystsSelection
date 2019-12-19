import itk
import sys
import os
import numpy
numpy.set_printoptions(threshold=sys.maxsize) #show entire array in numpy

path=input("Enter the path: ") #to sobstitute linking the previous code

Dim=3
PixelType=itk.F
LabelPixelType=itk.US #Change in US instead of UL 

ImageType=itk.Image[PixelType,Dim]
LabeledImageType=itk.Image[LabelPixelType,Dim]

MaskPixelType=itk.UC
MaskImageType=itk.Image[MaskPixelType,Dim]

#read the 4mm input volume
LabelReaderType=itk.ImageFileReader[LabeledImageType]
labelReader=LabelReaderType.New()
labelReader.SetFileName(path+"/T2.mha")

try:
    labelReader.Update()
except Exception:
    print("EXIT FAILURE")
    sys.exit(1)

#read the 4mm T2
FileReaderType=itk.ImageFileReader[ImageType]
reader4mm=FileReaderType.New()
reader4mm.SetFileName(path+"/T2.mha")

try:
    reader4mm.Update()
except Exception:
    print("EXIT FAILURE")
    sys.exit(1)

#define ouputimage
outputImage=labelReader.GetOutput() #works on the first implementation T2.mha

#read the masks and compute an overall masks
print("Reading mask1")
MaskImageFileReaderType=itk.ImageFileReader[MaskImageType]
maskReader1=MaskImageFileReaderType.New()
maskReader1.SetFileName(path+"/L.tif")
maskReader1.Update()

print("Reading mask2")
maskReader2=MaskImageFileReaderType.New()
maskReader2.SetFileName(path+"/R.tif")
maskReader2.Update()

MaximumFilterType=itk.MaximumImageFilter[MaskImageType,MaskImageType,MaskImageType]
maximumFilter=MaximumFilterType.New()
maximumFilter.SetInput1(maskReader1.GetOutput())
maximumFilter.SetInput2(maskReader2.GetOutput())

try:
    maximumFilter.Update()
except Exception as error:
    print(error)

maskImage=maximumFilter.GetOutput()

#flip in z direction

flipInput=1
if(flipInput): #if flipInput==1 enter
    FlipImageFilterType=itk.FlipImageFilter[MaskImageType]
    flipFilter=FlipImageFilterType.New()
    
    flipArray=itk.Index[Dim]()
    flipArray[0]=0
    flipArray[1]=0
    flipArray[2]=flipInput
    flipFilter.SetFlipAxes(flipArray)
    flipFilter.SetInput(maximumFilter.GetOutput())
    flipFilter.FlipAboutOriginOff()
        
    try:
        flipFilter.Update()
    except Exception as error:
        print(error)
    
maskImage=flipFilter.GetOutput()

OutputArray=itk.GetArrayViewFromImage(outputImage)

MaskArray=itk.GetArrayViewFromImage(maskImage)

print("Processing Pixel...")

z=0
y=0
x=0
for z in range(OutputArray.shape[0]):
    for y in range(OutputArray.shape[1]):
        for x in range(OutputArray.shape[2]):
            if (OutputArray[z][y][x]!=0):
                if(MaskArray[z][y][x]==0):
                    OutputArray[z][y][x]=0
                else:
                    OutputArray[z][y][x]=1

final=itk.GetImageViewFromArray(OutputArray)
final.SetOrigin(reader4mm.GetOutput().GetOrigin())
final.SetSpacing(reader4mm.GetOutput().GetSpacing())
final.SetDirection(reader4mm.GetOutput().GetDirection())

WriterType=itk.ImageFileWriter[LabeledImageType]
writer=WriterType.New()
writer.SetFileName(path+"/mask.mha")
writer.SetInput(final)
try:
    writer.Update();
except Exception as error:
    print("EXIT FAILURE")
    print(error)
    sys.exit(1)

print("EXIT SUCCESS")

