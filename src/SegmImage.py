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
    def __init__(self, filename,ClaNum):
        self.filename=filename
        self.ClaNum=ClaNum
        
        print "Class init ok"
#==========================================================
    def red_points(self,data, X, Y):
        points = []
        for (r,g,b), n in zip(data, count()):
            d = r-g-b
            if d != 0:
                points.append(self.Point(n % X, n // X, d))
        return points
#==========================================================
    def EllipseFitting(self):
    
        frames = [Image.open(self.filename).convert("RGB")]
        points_to_track = self.ClaNum
        k_or_guess = points_to_track
        X, Y = frames[0].size
        try:
            
            for im, n in zip(frames, count()):
                points = array([array([p.x, p.y], "f") for p in self.red_points(list(im.getdata()), X, Y)])
                if len(points) > 0:
                
                    codebook, distortion = vq.kmeans(points, k_or_guess)
                    print codebook, distortion 
                    draw = Draw(im)
                    assert points_to_track == len(codebook)
                    for p in codebook:
                        p = self.Point(int(p[0]), int(p[1]))
                        draw.line((p.x-10, p.y-10) + (p.x+10, p.y+10), fill=(255, 0, 0))
                        draw.line((p.x-10, p.y+10) + (p.x+10, p.y-10), fill=(255, 0, 0))
                        draw.ellipse((p.x-100, p.y-100, p.x+100, p.y+100),None, "blue")
                
                    print n,
                print
        finally:
            
            frames[0].show()       
   
   