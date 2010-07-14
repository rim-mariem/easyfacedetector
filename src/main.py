'''
Created on 14.07.2010
Cbk=0
    Crk=0
    CbBuf=0
    CrBuf=0
    for i in range(180,250):
        for j in range(180,250):
            Y,Cb,Cr = filter.output_color_space.getpixel((j, i))
            CbBuf=CbBuf+Cb
            CrBuf=CrBuf+Cr
            Cbk=Cbk+1
            Crk=Crk+1
            
    print "Cb= ",int(CbBuf/Cbk)
    print "Cr= ",int(CrBuf/Crk)



@author: aval
'''
from PreImage import PreImage 
if __name__ == '__main__':
    filter = PreImage ("faces.jpg")
    filter.convert('sw','YCbCr')
    filter.grey_scale('sw','YCbCr')
   
    
    