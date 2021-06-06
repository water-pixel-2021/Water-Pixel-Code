#
#E4FI AJOUT pour faire un preprocessing des images dont on a besoin dans "analysisQualitativeRun.py"
#

from skimage.morphology import area_opening
from skimage.morphology import area_closing

from imageio import imread 
from imageio import imsave

def doPreprocessing(inputPath, outputPath):
    image=imread(inputPath)
    imgProcessed=area_opening(image,2)
    imgProcessed=area_closing(imgProcessed,2)
    imsave(outputPath, imgProcessed,'png')

doPreprocessing("./Images/2D/fig1.jpg", "./Images/2D/fig1bis.png")

doPreprocessing("./Images/2D/fig2.jpg", "./Images/2D/fig2bis.png")



