import os
import itk

Dimension=3
PixelType=itk.F
ImageType=itk.Image[PixelType,Dimension]

path=input("Enter the name folder that contains T2 and T2.mha")

dicomDirectoryName=path+"/T2"
outputImageFileName=path+"/T2.mha"

print("Reading image series")

#ReaderType=itk.ImageSeriesReader[ImageType]
#reader=ReaderType.New()

#ImageIOType=itk.GDCMImageIO
#dicomIO=ImageIOType.New()
#reader.SetImageIO(dicomIO)


NamesGeneratorType=itk.GDCMSeriesFileNames
nameGenerator=NamesGeneratorType.New()
nameGenerator.SetUseSeriesDetails(True);
nameGenerator.RecursiveOn();
nameGenerator.SetDirectory(dicomDirectoryName);

seriesUID=nameGenerator.GetSeriesUIDs()
   
    
if len(seriesUID)<1:
        print("No DICOMs")
for uid in seriesUID:
        seriesIdentifier=uid
        print("Reading: "+seriesIdentifier)
        fileNames=nameGenerator.GetFileNames(seriesIdentifier)
        
        reader = itk.ImageSeriesReader[ImageType].New()
        dicomIO = itk.GDCMImageIO.New()
        reader.SetImageIO(dicomIO)
        reader.SetFileNames(fileNames)
    #   reader.ForceOrthogonalDirectionOff()

        writer = itk.ImageFileWriter[ImageType].New()
                         
        writer.SetInput(reader.GetOutput())
        writer.SetFileName(outputImageFileName)
        writer.UseCompressionOn()
        writer.Update()
print("File T2.mha Created")






