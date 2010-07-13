import Image

if __name__ == '__main__':

    cbcr = [0,0,0]
    input_image = Image.open("lena.jpg")
    width, height = input_image.size
    size = input_image.size
    output_image = Image.new("RGB", size)
    for i in range(height):
        for j in range (width):
            rgb = input_image.getpixel((j,i))
            cbcr[0] =  int(0.299*rgb[0] + 0.587*rgb[1] + 0.114*rgb[2]) #Y
            cbcr[1] =  int((rgb[2] - cbcr[0])*0.564 + 128) #Cb
            cbcr[2] =  int((rgb[0] - cbcr[0])*0.713 + 128) #Cr
            output_image.putpixel((j, i),tuple(cbcr))
            
    output_image.show()
    output_image.save("lena4.jpg", "JPEG")
    print "\t==== converting ok ===="
    
    
