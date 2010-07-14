import Image

class PreImage (object):
    
    def __init__ (self, input_image_name):
        self.input_image = Image.open(input_image_name)
        self.width, self.height = self.input_image.size
        size = self.input_image.size
        self.output_color_space = Image.new("RGB", size)
        self.output_grey_scale = Image.new("RGB", size)
        print "\t==== class init ok ===="
    
    def convert (self, mode):
        cbcr = [0,0,0]
        for i in range(self.height):
            for j in range (self.width):
                rgb = self.input_image.getpixel((j,i))
                cbcr[0] =  int(0.299*rgb[0] + 0.587*rgb[1] + 0.114*rgb[2]) #Y
                cbcr[1] =  int((rgb[2] - cbcr[0])*0.564 + 128) #Cb
                cbcr[2] =  int((rgb[0] - cbcr[0])*0.713 + 128) #Cr
                self.output_color_space.putpixel((j, i),tuple(cbcr))
        print "\t==== converting ok ===="
        if mode == 's':
            self.output_color_space.show()
        elif mode == 'w':
            self.output_color_space.save("lena4.jpg", "JPEG")
        elif mode == 'sw':
            self.output_color_space.show()
            self.output_color_space.save("lena4.jpg", "JPEG")
        else:
            print "Invalid mode. mode mast be s, w, or sw"
    

    
a = PreImage ("lena2.jpg")
a.convert('sw')
