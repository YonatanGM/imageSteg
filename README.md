# imageSteg

Python program to hide files in images using the LSB steganography technique. A colour pixel is composed of red, green and blue, encoded on one byte. The idea is to store information in the first bit of every pixel's RGB component. 

## Install
You just need the Python Image Library (Pillow) 

`pip install -r requirements.txt`

## Usage
run main.py and a window will pop up
![interface](imageSteg/step.PNG)
