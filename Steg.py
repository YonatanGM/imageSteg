from PIL import Image as img
from image import IMG
from file import FILE
from tkinter import *

class STEG(IMG, FILE):
    def __init__(self, img_path, file_path=None):
        IMG.__init__(self, img_path)
        FILE.__init__(self, file_path)


    def RGB_hide(self):
        '''
        Replace the least-significant bit for RGB images.
        :param payload: This is the path of the payload file.
        '''
        # 3 bytes per pixel should be greater than 2* the binary message length
        if self.img_size*3 <= 2*self.file_size:
            raise Exception('[!] Attempting to hide a message that is too large for the carrier')

        # generate bitstream 
        bitstream = iter(self.text_to_binary(self.img_size * 3))
            # create a new empty image the same size and mode as the original
        newIm = img.new("RGB", (self.img.size[0], self.img.size[1]), "white") 
        try:
            for row in range(self.img.size[1]):
                for col in range(self.img.size[0]):
                    # get the value for each byte of each pixel in the original image
                    r,g,b = self.img.getpixel((col,row))

                    # get the new lsb value from the bitstream
                    rb = next(bitstream)
                    # modify the original byte with our new lsb
                    r = self.set_bit(r, rb)
                    gb = next(bitstream)
                    fgg = self.set_bit(g, gb)
                    bb = next(bitstream)
                    fgb = self.set_bit(b, bb)
                    # add pixel with modified values to new image
                    newIm.putpixel((col, row),(r, g, b))
            output_file_type = self.assign_output_type()
            newIm.save(str('new.' + output_file_type), output_file_type)
            print('[+] {} created'.format('new.' + output_file_type))
        except Exception as e:
            raise Exception('Failed to write new file: {}'.format(str(e)))

    # extract hidden message from RGB image
    def RGB_extract(self, output_file_name):
        '''
        Extracts and reconstructs payloads concealed in RGB images.
        :param fg: This is the PngImageFile of the carrier image.
        '''
        hidden = ''
        try:
            # iterate through each pixel and pull the lsb from each color per pixel
            for row in range(self.img.size[1]):
                for col in range(self.img.size[0]):
                    fgr,fgg,fgb = self.img.getpixel((col,row))
                    
                    hidden += bin(fgr)[-1]
                    hidden += bin(fgg)[-1]
                    hidden += bin(fgb)[-1]
            try:
                returned_file = self.binary_to_text(hidden, output_file_name)
                return returned_file
            except Exception as e:
                raise Exception('Inner failed to extract message: {}'.format(str(e)))
        except Exception as e:
            raise Exception('Outer failed to extract message: {}'.format(str(e)))   

    def RGBA_hide(self):
        '''
        Replace the least-significant bit for RGBA images.
        :param payload: This is the path of the payload file.
        '''
        if self.img_size*3 <= 2*self.file_size:
            raise Exception('[!] Attempting to hide a message that is too large for the carrier')
        # generate bitstream 
        bitstream = iter(self.text_to_binary(self.img_size * 3))

        newIm = img.new("RGBA", (self.img.size[0], self.img.size[1]), "white") 
        try:
            for row in range(self.img.size[1]):
                for col in range(self.img.size[0]):
                    fgr, fgg, fgb, fga = self.img.getpixel((col, row))

                    redbit = next(bitstream)
                    fgr = self.set_bit(fgr, redbit)

                    greenbit = next(bitstream)
                    fgg = self.set_bit(fgg, greenbit)

                    bluebit = next(bitstream)
                    fgb = self.set_bit(fgb, bluebit)
                    # add pixel to new image
                    newIm.putpixel((col, row),(fgr, fgg, fgb, fga))
            output_file_type = self.assign_output_type()
            newIm.save(str('new.' + output_file_type), output_file_type)
            self.output_file_type = output_file_type
            print('[+] {} created'.format('new.' + output_file_type))
        except Exception as e:
            raise Exception('[!] Failed to write new file: {}'.format(str(e)))
        

    def RGBA_extract(self, output_file_name):
        '''
        Extracts and reconstructs payloads concealed in RGBA images.
        :param fg: This is the PngImageFile of the carrier image.
        '''
        hidden = ''
        try:
            # iterate through each pixel and pull the lsb from each color per pixel
            for row in range(self.img.size[1]):
                for col in range(self.img.size[0]):
                    fgr, fgg, fgb, fga = self.img.getpixel((col, row))
                    
                    hidden += bin(fgr)[-1]
                    hidden += bin(fgg)[-1]
                    hidden += bin(fgb)[-1]
            try:
                returned_file = self.binary_to_text(hidden, output_file_name)
                return returned_file
            except Exception as e:
                raise Exception('Inner failed to extract message: {}'.format(str(e)))
        except Exception as e:
            raise Exception('Outer failed to extract message: {}'.format(str(e)))

    def L_hide(self):
        # 3 bytes per pixel should be greater than 2* the binary message length
        if self.img_size*3 <= 2*self.file_size:
            raise Exception('[!] Attempting to hide a message that is too large for the carrier')

        # generate bitstream 
        bitstream = iter(self.text_to_binary(self.img_size * 3))

        newIm = img.new("L", (self.img.size[0], self.img.size[1]), "white") 
        try:
            for row in range(self.img.size[1]):
                for col in range(self.img.size[0]):
                    fgL = self.img.getpixel((col,row))

                    nextbit = next(bitstream)
                    fgL = self.set_bit(fgL, nextbit)

                    # add pixel to new image
                    newIm.putpixel((col,row),(fgL))
            output_file_type = self.assign_output_type()
            newIm.save(str('new.' + output_file_type), output_file_type)
            print('[+] {} created'.format('new.' + output_file_type))
        except Exception as e:
            raise Exception('Failed to write new file: {}'.format(str(e)))

    def L_extract_message(self, output_file_name):
        hidden = ''
        try:
            # iterate through each pixel and pull the lsb from each color per pixel
            for row in range(self.img.size[1]):
                for col in range(self.img.size[0]):
                    fgL = self.img.getpixel((col,row))
                    
                    hidden += bin(fgL)[-1]
            try:
                returned_file = self.binary_to_text(hidden, output_file_name)
                return returned_file
            except Exception as e:
                raise Exception('Inner failed to extract message: {}'.format(str(e)))
        except Exception as e:
            raise Exception('Outer failed to extract message: {}'.format(str(e)))
        
    def hide(self):
        
        if self.img_mode == 'L':
            self.L_hide()
        elif self.img_mode in ['RGB', 'BGR']:
            self.RGB_hide()
        elif self.img_mode == 'RGBA':
            self.RGBA_hide()
        elif self.img_mode == '1':
            print("[!] Cannot hide content using an image with a mode of '1'")
        else:
            print("[!] Error determining image mode")

    def extract(self, output_file_name = 'hidden'):
        if self.img_mode == 'L':
            self.L_extract(output_file_name)
        elif self.img_mode in ['RGB', 'BGR']:
            self.RGB_extract(output_file_name)
        elif self.img_mode == 'RGBA':
            self.RGBA_extract(output_file_name)
        elif self.img_mode == '1':
            print("[!] Cannot hide content using an image with a mode of '1'")
        else:
            print("[!] Error determining image mode")

    def display_text(text):
        text.insert(INSERT, "hiding message...\n")
        text.pack()
        
    
      

                        
