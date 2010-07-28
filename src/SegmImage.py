from __future__ import division


from scipy import *
from scipy.cluster import vq
from itertools import count
from ImageDraw import Draw
import Image



class SegmImage(object):
    class Point(object):
        """
            Three dimensional vector: <x, y, intensity>
        """
        def __init__(self, x, y, intensity=0):
            self.x = x
            self.y = y
            self.intensity = intensity
            
#==========================================================
    def __init__(self, image ,ClaNum):
        #self.filename=filename
        
        self.image = image
        self.ClaNum=ClaNum
        self.Clusters = 0
        self.por=0
        print "\t==== class SegmImage init ok ===="
#==========================================================
    def red_points(self,data, X, Y):
        points = []
        for (r,g,b), n in zip(data, count()):
            d = r-g-b
            if r==255&g==255&b==255:
                points.append(self.Point(n % X, n // X, d))
            
        return points
#==========================================================
    def UnionClasters(self,points):
    
        res =[]
        temp=[]
        for i in range(len(points)):
            temp.append((int(points[i][0]), int(points[i][1])))
    
        while temp:
            now = temp[0]
            t = []
            for j in range(1,len(temp)):
                d= (now[0]-temp[j][0])**2 + (now[1]-temp[j][1])**2
                d = int(pow(d, 0.5))
                t.append([temp[j][0], temp[j][1], d])
    
            for a in range(len(t)):
                k=t[a]
                for j in range(a+1,len(t)):
                    if k[2] < t[j][2]:
                        t[a] = t[j]
                        t[j] = k
                        k=t[a]
        
            srx=now[0]
            sry=now[1]
            count = 1
    
            temp2 =[]
            temp2[len(temp2):] = [(now[0], now[1])] 
    
            # t- in sort
            for a in range (len(t)):
                if t[a][2]<=self.por:
                    srx = srx + t[a][0]
                    sry = sry + t[a][1]
                    count = count +1
                    temp2[len(temp2):] = [(t[a][0], t[a][1])] 
            x= int(srx/count)
            y= int(sry/count)
    
            res.append ([x,y])
    
            temp = [el for el in temp if el not in temp2]
    
        
        return res
#==========================================================
    def EllipseFitting(self,mode):
    
        #img = Image.open(self.filename)
        frames = [self.image]
                
        width, height = self.image.size
        white = 0
        ful=width*height
        
        for i in range(height):
            for j in range (width):
                rgb = self.image.getpixel((j,i))
                if rgb!=0:
                    white=white+1
                    
        self.por=int((white/ful)*170)
        
        #if self.por<100:
        #    self.por = 200
        #elif self.por>400:
        #    self.por=400
        
        print "\t==== all pixels = ", ful, " ===="
        print "\t==== white pixels = ", white, " ===="
        print "\t==== threshold sensitivity is = ", self.por, " ===="
         
        print "\t==== Begining find clusters... ===="
        
        img = self.image.convert("RGB")
        frames = [img]             
                     
        
        points_to_track = self.ClaNum
        k_or_guess = points_to_track
        X, Y = frames[0].size
        try:
            
            for im, n in zip(frames, count()):
                points = array([array([p.x, p.y], "f") for p in self.red_points(list(im.getdata()), X, Y)])
                if len(points) > 0:
                
                    codebook, distortion = vq.kmeans(points, k_or_guess)
                     
                    draw = Draw(im)
                    assert points_to_track == len(codebook)
                    delt=int(distortion)
                    
                    res = self.UnionClasters(codebook)
                    self.Clusters = res
                    for p in res:
                        draw.line((p[0]-10, p[1]-10) + (p[0]+10, p[1]+10), fill=(255, 0, 0))
                        draw.line((p[0]-10, p[1]+10) + (p[0]+10, p[1]-10), fill=(255, 0, 0))
                        draw.ellipse((p[0]-(int(self.por/2)), p[1]-(int(self.por/2)), p[0]+(int(self.por/2)), p[1]+(int(self.por/2))), None, "blue")                
                   
                           
                    
                print
        finally:
            
            if mode=='s':
                frames[0].show()
                   
   
   