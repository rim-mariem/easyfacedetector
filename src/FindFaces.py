'''
Created on 28.07.2010

@author: aval
'''

import Image
import ImageDraw

class FindFaces(object):
    '''
    classdocs
    '''

    def __init__(self, hsv, cbcr, image):
        '''
        Constructor
        '''
        self.hsv = hsv
        self.cbcr = cbcr
        self.image = image
        print "\t==== class FindFaces init ok ====" 
    
    def Faces(self):
        d = []
        temp=0
        por_max = 150
        min_max = [[[0, 0], 1000], [[0, 0], 0]]
        rec_coordinates =[]
    
    
        for i in self.cbcr:
            rec_coordinates=[]
            for j in self.hsv:
                temp = (i[0]-j[0])**2 + (i[1]-j[1])**2
                temp = int(pow(temp, 0.5))
                if temp<por_max:
                    d.append([j,temp])
                    
            for k in d:
                if k[1]>min_max[1][1]:
                    min_max[1] = k
                if k[1]<min_max[0][1]:
                    min_max[0] = k
        
                 
            
          
        
            print min_max
            
            if min_max[0][0][1]!=min_max[1][0][1]:
                x1_cor = min_max[0][0][0] - min_max[0][1]
                y1_cor = min_max[0][0][1] 
                x2_cor = min_max[1][0][0] + min_max[0][1]
                y2_cor = min_max[1][0][1]
                rec_coordinates.append([[x1_cor,y1_cor],[x2_cor, y2_cor]])
        
            else:
                x1_cor = min_max[0][0][0] - min_max[0][1]
                y1_cor = i[1]
                x2_cor = min_max[1][0][0] + min_max[0][1]
                y2_cor = min_max[1][0][1]
                rec_coordinates.append([[x1_cor,y1_cor],[x2_cor, y2_cor]])
                   
            
               
    
   
        
        print "rec_coordinates=", rec_coordinates
        
        draw = ImageDraw.Draw(self.image)
        
        for i in rec_coordinates:
            if i[0][1]>i[1][1]:
                j = i[0][1]
                i[0][1] = i[1][1]
                i[1][1] = j 
            print "rec_coordinates=", i 
            draw.ellipse((i[0][0],i[0][1],i[1][0],i[1][1]), None, "blue")
        
        self.image.show()   
    
    