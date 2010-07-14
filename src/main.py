'''
Created on 14.07.2010

@author: aval
'''
from PreImage import PreImage 
if __name__ == '__main__':
    filter = PreImage ("lena3.jpg")
    filter.convert('sw','YCbCr')
    filter.grey_scale('sw','YCbCr')
    