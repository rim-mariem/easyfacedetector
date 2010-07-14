'''
Created on 14.07.2010

@author: aval
'''

import Image

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
    def __init__ (self, input_image_name):
        self.input_image = Image.open(input_image_name)
        self.width, self.height = self.input_image.size
        size = self.input_image.size
        self.output_color_space = Image.new("RGB", size)
        self.output_grey_scale = Image.new("RGB", size)
        print "\t==== class init ok ===="
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
        hsv = [0,0,0]
        r,g,b = rgb
        max = r
        if max<g:
            max = g
        if max<b:
            max=b
        min = r
        if min>g:
            min = g
        if min>b:
            min=b
        if max == 0:
            hsv[1]=0
            hsv[2]=0
        else:
            hsv[2]=max
            hsv[1]=int((max-min)/max)
        if (hsv[2] == r)&(g>=b):
            #print max-min
            hsv[0]= int((60*(g-b))/(hsv[1]+1))
        elif (hsv[2] == r)&(g<b):
            hsv[0]= int((60*(g-b))/(hsv[1]+1))+360  
        elif hsv[2] == g:
            hsv[0]= int((60*(b-r))/(hsv[1]+1))+120
        else:
            hsv[0]= int((60*(r-g))/(hsv[1]+1))+240
        
        hsv[0] = int(hsv[0]/2)
        hsv[1] = hsv[1]*255
        hsv[2] = hsv[2]*255
        return hsv
    #=============================================================    
    def RGB2STOC (self,rgb):
        '''
            convert one pixel from RGB to chromatic color
            space                                   
        '''        
        stoc = [0,0,0]
        r,g,b = rgb
        stoc[0] = r/(r+g+b)
        stoc[1] = g/(r+g+b)
        stoc[2] = 1 - stoc[0]-stoc[1]
        
        print rgb, stoc
        return stoc
     
    #=============================================================
    def YCbCr2GREY (self,rgb):
        '''
            convert one pixel from YCbCr to grey skin color model                                   
        '''        
        grey = [0,0,0]
        if ((rgb[1]>90)&(rgb[1]<170))&((rgb[2]>90)&(rgb[2]<170)):
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
                self.output_color_space.putpixel((j, i),tuple(cbcr))
        print "\t==== converting to YCbCr ok ===="
    #=============================================================
    def convert_to_HSV (self):
        '''
           convert all image from RGB to HSV                                 
        '''    
        hsv = [0,0,0]
        for i in range(self.height):
            for j in range (self.width):
                rgb = self.input_image.getpixel((j,i))
                hsv = self.RGB2HSV(rgb)
                self.output_color_space.putpixel((j, i),tuple(hsv))
        print "\t==== converting to HSV ok ===="
    #=============================================================
    def convert_to_STOC (self):
        '''
           convert all image from RGB to HSV                                 
        '''    
        stoc = [0,0,0]
        for i in range(self.height):
            for j in range (self.width):
                rgb = self.input_image.getpixel((j,i))
                stoc = self.RGB2STOC(rgb)
                self.output_color_space.putpixel((j, i),tuple(stoc))
        print "\t==== converting to STOC ok ===="
    #===============================================================
    def YCbCr_to_grey_scale (self):
        '''
           convert all image from YCbCr to grey skin color model                                   
        '''    
        for i in range(self.height):
            for j in range (self.width):
                rgb = self.input_image.getpixel((j,i))
                grey = self.YCbCr2GREY(rgb)
                self.output_grey_scale.putpixel((j, i),tuple(grey))
        print "\t==== converting from YCbCr to grey scale ok ===="
    #===============================================================
    def convert (self, mode, color_space):
        '''
            convert from RGB image to some color space                                  
        '''    
        if color_space == 'YCbCr':
            self.convert_to_YCbCr()
            if mode == 's':
                self.output_color_space.show()
            elif mode == 'w':
                self.output_color_space.save("temp_cs.jpg", "JPEG")
            elif mode == 'sw':
                self.output_color_space.show()
                self.output_color_space.save("temp_cs.jpg", "JPEG")
            elif mode == '':
                print ""
            else:
                print "Invalid mode. mode mast be s, w, or sw"
        elif color_space == 'HSV':
            self.convert_to_HSV()
            if mode == 's':
                self.output_color_space.show()
            elif mode == 'w':
                self.output_color_space.save("temp_cs.jpg", "JPEG")
            elif mode == 'sw':
                self.output_color_space.show()
                self.output_color_space.save("temp_cs.jpg", "JPEG")
            elif mode == '':
                print ""
            else:
                print "Invalid mode. mode mast be s, w, or sw"
        elif color_space == 'STOC':
            self.convert_to_STOC()
            if mode == 's':
                self.output_color_space.show()
            elif mode == 'w':
                self.output_color_space.save("temp_cs.jpg", "JPEG")
            elif mode == 'sw':
                self.output_color_space.show()
                self.output_color_space.save("temp_cs.jpg", "JPEG")
            elif mode == '':
                print ""
            else:
                print "Invalid mode. mode mast be s, w, or sw"
        else: 
            print "Invalid color space. It most be YCbCr, HSV"
    #==========================================================
    def grey_scale (self, mode, color_space):
        '''
            convert from some color space to grey skin color model                                  
        '''    
        if color_space == 'YCbCr':
            self.YCbCr_to_grey_scale()
            if mode == 's':
                self.output_grey_scale.show()
            elif mode == 'w':
                self.output_grey_scale.save("temp_gr.jpg", "JPEG")
            elif mode == 'sw':
                self.output_grey_scale.show()
                self.output_grey_scale.save("temp_gr.jpg", "JPEG")
            elif mode == '':
                print ""
            else:
                print "Invalid mode. mode mast be s, w, or sw"
        elif color_space == 'HSV':
            print "HSV not supported now"
        else: 
            print "Invalid color space. It most be YCbCr, HSV"
        
        


