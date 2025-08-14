# The purpose of this program is to convert PNG
# images from fx. https://www.pixilart.com/ to the
# 1.8" TFT RGB565 format.
#
# Tools -> Manage packages
# Search for "Pillow", install in Local Python.
#
# Put all PNGs in the same directory and run the program.
#
import os, sys, pathlib
from PIL import Image

all_files = os.listdir()
#all_files = ["ball.png"]
for f in all_files:
    if pathlib.Path(f).suffix != ".png":
        continue
    
    print(f"Converting: {f}")
    im = Image.open(f)
    width, height = im.size
    if width > 160 or height > 128:
        print("Image won't fit on screen, just so you know")

    data = bytearray(2+width*height*2)
    ptr = 0

    # Mask is a 1 bit/pixel / 1 byte/8 pixels black and white version of
    mask_width = width//8 if width//8 == width/8 else width//8+1
    mask_height = height
    mask = bytearray(2+mask_width*mask_height)
    mask_ptr = 0
    mask_bit_ptr = 0
    for x in range(width):
        for y in range(height):
            # pixel is a (R,G,B,T) tuple
            pixel = im.getpixel((x,y))
            r = pixel[0]
            g = pixel[1]
            b = pixel[2]
            t = pixel[3]
            rgb565 = ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)
            data[ptr] = rgb565 & 0xFF
            data[ptr+1] = (rgb565 >> 8) & 0xFF
            ptr += 2
            # Could also be calculated, but why bother?
            #data[x*2+y*height*2] = rgb565 & 0xFF
            #data[x*2+y*height*2+1] = (rgb565 >> 8) & 0xFF
            
            # Mask - id alpha channel not fully transparent - make a collision spot.
            #print(mask_ptr, mask_bit_ptr,t,mask_width, mask_height)
            if t == 255:
                mask[mask_ptr] = mask[mask_ptr] | (0x1 << 7-(mask_bit_ptr))
            mask_bit_ptr = (mask_bit_ptr + 1) % 8
            if mask_bit_ptr == 0:
                #print(hex(mask[mask_ptr]))
                mask_ptr += 1


    # Save width and height as last two bytes.
    data[-2] = width & 0xFF
    data[-1] = height & 0xFF
    print(f"Writing {pathlib.Path(f).stem}.rgb")
    with open(pathlib.Path(f).stem+".rgb", "wb") as binary_file:
        # Write bytes to file
        binary_file.write(data)

    # Save mask
    print(f"Writing {pathlib.Path(f).stem}.mask")
    with open(pathlib.Path(f).stem+".mask", "wb") as binary_file:
        # Write bytes to file
        binary_file.write(mask)
    mask[-2] = mask_width & 0xFF
    mask[-1] = mask_height & 0xFF
    #print(mask)
# Check array is filled right:
#    4x4
#    0 1 2 3, 0  -> 0+0, 2+0, 4+0, 6+0
#    0 1 2 3, 1  -> 0+1*4*2, 2+8, 4+8, 6+8
#    0 1 2 3, 2  -> 0+2*4*2, 2+16, ...
#    0 1 2 3, 3  -> ..., ..., ..., 6+24
#
# Pixels:
# 15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,0
#  R, R, R, R, R, G,G,G,G,G,G,B,B,B,B,B