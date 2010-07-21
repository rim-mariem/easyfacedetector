'''
Created on 14.07.2010

@author: aval
'''
from PreImage import PreImage 
from SegmImage import SegmImage


if __name__ == '__main__':
    filter = PreImage()
    filter.convert('','YCbCr')
    filter.grey_scale('w','YCbCr')
    #"temp_gr_YCbCr.jpg"
    filter2 = SegmImage ("temp_gr_YCbCr.jpg",ClaNum=5)
    filter2.EllipseFitting()
    
   



    
    
   
    
    