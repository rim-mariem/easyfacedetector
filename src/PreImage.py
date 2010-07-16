'''
Created on 14.07.2010

@author: aval
'''

import Image
from VideoCapture import Device

class PreImage (object):
    '''
        This class using for preparatin input image.
        It convert RGB input image into some color 
        space (YCbCr, HSV, etc). And then transform 
        a color image from that color space into a 
        grey scale image such that the gray value at 
        each pixel shows the likelihood of the pixel 
        belonging to the skin.
        input_image - buffer for input image
        width, height - sizes of input image
        output_color_space - buffer for image which 
                             contain some color space
        output_color_space - buffer for grey scale image
                                        
    '''
    def __init__ (self):
        cam = Device()
        print "\t==== getting image from camera ===="
        print "\t==== getting image success===="
        self.input_image_buf = cam.getImage()
        self.input_image=self.input_image_buf.resize((320,240))
        self.width, self.height = self.input_image.size
        size = self.input_image.size
        self.output_YCbCr_color_space = Image.new("RGB", size)
        self.output_YCbCr_grey_scale = Image.new("L", size)
        self.output_HSV_color_space= Image.new("L", size)
        self.output_HSV_grey_scale = Image.new("L", size)
        print "\t==== class PreImage init ok ===="
    #=============================================================    
    def RGB2YCbCr (self,rgb):
        '''
            convert one pixel from RGB to YCbCr                                   
        '''        
        cbcr = [0,0,0]
        cbcr[0] =  int(0.299*rgb[0] + 0.587*rgb[1] + 0.114*rgb[2]) #Y
        cbcr[1] =  int((rgb[2] - cbcr[0])*0.564 + 128) #Cb
        cbcr[2] =  int((rgb[0] - cbcr[0])*0.713 + 128) #Cr
        return cbcr
    #=============================================================    
    def RGB2HSV (self,rgb):
        '''
            convert one pixel from RGB to HSV                                   
        '''        
        hsv = [0,0.0,0.0]
        r,g,b = rgb
        r=(float(r)/255.0)
        g=(float(g)/255.0)
        b=(float(b)/255.0)
        maxc = max(r,g,b)
        minc = min(r,g,b)
        v = maxc
        if minc==maxc: 
            hsv[0]=0
            hsv[1]=0.0
            hsv[2]=v
            return hsv 
        s = (maxc-minc) / maxc
        rc = (maxc-r) / (maxc-minc)
        gc = (maxc-g) / (maxc-minc)
        bc = (maxc-b) / (maxc-minc)
        if r == maxc: 
            h = bc-gc
        elif g == maxc: 
            h = 2.0+rc-bc
        else: 
            h = 4.0+gc-rc
        h = (h/6.0) % 1.0
        h=int(h*360)
        
        hsv[0]=int(h-255)
        if hsv[0]<0:
            hsv[0]=0
                    
        hsv[1]=s
        hsv[2]=v
        return hsv 
    #=============================================================
    def YCbCr2GREY (self,rgb):
        '''
            convert one pixel from YCbCr to grey skin color model                                   
        '''        
      
        if ((rgb[1]>90)&(rgb[1]<150))&((rgb[2]>90)&(rgb[2]<150)):
            grey = 0
        else:
            grey = 255
        
        
        return grey      
    #=============================================================
    def HSV2GREY (self,rgb):
        '''
            convert one pixel from YCbCr to grey skin color model                                   
        '''        
        grey = [0,0,0]
        print rgb
        if rgb==0:
            grey = [255,255,255]
        else:
            grey = [0,0,0] 
        return grey        
    #=============================================================
    def convert_to_YCbCr (self):
        '''
           convert all image from RGB to YCbCr                                 
        '''    
        cbcr = [0,0,0]
        for i in range(self.height):
            for j in range (self.width):
                rgb = self.input_image.getpixel((j,i))
                cbcr = self.RGB2YCbCr(rgb)
                self.output_YCbCr_color_space.putpixel((j,i),tuple(cbcr))
                                
                rgb2=self.input_image.getpixel((j,i))
                                       
                self.YCbCr_to_grey_scale(j,i,cbcr)
                
                                             
        print "\t==== converting to YCbCr ok ===="
        print "\t==== converting from YCbCr to grey scale ok ===="
    
    #=============================================================
    def YCbCr_to_grey_scale(self,x,y,rgb):
              
        grey = self.YCbCr2GREY(rgb)
        self.output_YCbCr_grey_scale.putpixel((x,y),grey)
        
   #===============================================================    
    def convert_to_HSV (self):
        '''
           convert all image from RGB to HSV                                 
        '''    
        hsv = [0,0,0]
        for i in range(self.height):
            for j in range (self.width):
                rgb = self.input_image.getpixel((j,i))
                hsv = self.RGB2HSV(rgb)
                self.output_HSV_color_space.putpixel((j, i),hsv[0])
                self.HSV_to_grey_scale(j,i,hsv[0])
        print "\t==== converting to HSV ok ===="
        print "\t==== converting from HSV to grey scale ok ===="
   
    #===============================================================
    def HSV_to_grey_scale(self,x,y,hue):
        '''
           convert all image from YCbCr to grey skin color model                                   
        '''    
        temp = hue
        if temp == 0:
            temp = 255
        else:
            temp = 0
        self.output_HSV_grey_scale.putpixel((x, y),temp)
        
    #===============================================================
    def convert (self, mode, color_space):
        '''
            convert from RGB image to some color space                                  
        '''    
        if color_space == 'YCbCr':
            self.convert_to_YCbCr()
            if mode == 's':
                self.output_YCbCr_color_space.show()
            elif mode == 'w':
                self.output_YCbCr_color_space.save("temp_cs_YCbCr.jpg", "JPEG")
            elif mode == 'sw':
                self.output_YCbCr_color_space.show()
                self.output_YCbCr_color_space.save("temp_cs_YCbCr.jpg", "JPEG")
            elif mode == '':
                print ""
            else:
                print "Invalid mode. mode mast be s, w, or sw"
        elif color_space == 'HSV':
            self.convert_to_HSV()
            if mode == 's':
                self.output_HSV_color_space.show()
            elif mode == 'w':
                self.output_HSV_color_space.save("temp_cs_HSV.jpg", "JPEG")
            elif mode == 'sw':
                self.output_HSV_color_space.show()
                self.output_HSV_color_space.save("temp_cs_HSV.jpg", "JPEG")
            elif mode == '':
                print ""
            else:
                print "Invalid mode. mode mast be s, w, or sw"
        elif color_space == 'STOC':
            print "Stochastic model not supported now"
            
        else: 
            print "Invalid color space. It most be YCbCr, HSV"
    #==========================================================
    def grey_scale (self, mode, color_space):
        '''
            convert from some color space to grey skin color model                                  
        '''    
        if color_space == 'YCbCr':
            
            if mode == 's':
                self.output_YCbCr_grey_scale.show()
            elif mode == 'w':
                self.output_YCbCr_grey_scale.save("temp_gr_YCbCr.jpg", "JPEG")
            elif mode == 'sw':
                self.output_YCbCr_grey_scale.show()
                self.output_YCbCr_grey_scale.save("temp_gr_YCbCr.jpg", "JPEG")
            elif mode == '':
                print ""
            else:
                print "Invalid mode. mode mast be s, w, or sw"
        elif color_space == 'HSV':
            if mode == 's':
                self.output_HSV_grey_scale.show()
            elif mode == 'w':
                self.output_HSV_grey_scale.save("temp_gr_HSV.jpg", "JPEG")
            elif mode == 'sw':
                self.output_HSV_grey_scale.show()
                self.output_HSV_grey_scale.save("temp_gr_HSV.jpg", "JPEG")
            elif mode == '':
                print ""
            else:
                print "Invalid mode. mode mast be s, w, or sw"
        else: 
            print "Invalid color space. It most be YCbCr, HSV"
        
        


