'''
Created on 14.07.2010

@author: aval
'''

import Image
from VideoCapture import Device

from PreImage import PreImage 
from SegmImage import SegmImage
from FindFaces import FindFaces

if __name__ == '__main__':
   
    cam = Device()
    print "\t==== Camera initial ok ===="
    input_buf = cam.getImage()
    print "\t==== Getting image ok ===="
    image=input_buf.resize((100,80))   
    print "\t==== Resizing image ok ===="
    
    
        
    filterHSV = PreImage(image)
    filterYCbCr= PreImage(image)
    
    filterHSV.convert('','HSV')
    filterYCbCr.convert('','YCbCr')
    
    filterHSV.grey_scale('','HSV')
    filterYCbCr.grey_scale('','YCbCr')
    
    
    filterHSV2 = SegmImage (filterHSV.output_HSV_grey_scale,ClaNum=5)
    filterYCbCr2 = SegmImage (filterYCbCr.output_YCbCr_grey_scale,ClaNum=5)
    
    filterHSV2.EllipseFitting(mode = '')
    filterYCbCr2.EllipseFitting(mode = '')
    
    hsv = filterHSV2.Clusters
    cbcr = filterYCbCr2.Clusters
    
    image.save("me.jpg", "JPEG")
    
    print "\t==== HSV clusters center is = ", hsv, " ===="
    print "\t==== CbCr clusters center is = ", cbcr, " ===="
    
    #hsv = [[341, 129], [228, 190]]
    #cbcr = [[329, 192], [332, 417], [265, 256]]
    
    #image = Image.open("me.jpg").convert("RGB") 
    
    
    faces = FindFaces(hsv,cbcr,image)
    faces.Faces()    



    
    
   
    
    