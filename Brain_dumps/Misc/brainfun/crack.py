#!/usr/bin/python

# from PIL import Image

# background = Image.open("brainfun.png")

# background = background.convert("RGBA")

# new_img = Image.blend(background, overlay, 0.5)
# new_img.save("new.png","PNG")



# Image Compression from reduced single value decomposition
# Jordan Brown 
# 20th June 2016

# run convert -delay 20 -loop 0 *.jpg svd.gif to make the gif


from multiprocessing import Pool
from PIL import Image
import numpy as np
import scipy.misc
from copy import deepcopy
import cPickle
import gzip

import base64

def extract_band(band, img):
	'''
		Extract the RGB bands from an image
		0 == Red
		1 == Green
		2 == Blue
	'''
	imgmat = np.array(list(img.getdata(band=band)), int)
	imgmat.shape = (img.size[1], img.size[0])
	imgmat = np.matrix(imgmat)
	return imgmat

def get_RGB_matricies(img):
	'''
		Get the Red, Green and Blue image
		matricies
	'''
	return [extract_band(x, img) for x in range(3)]



def save_zipped_pickle(obj, filename, protocol=-1):
    with gzip.open(filename, 'wb') as f:
        cPickle.dump(obj, f, protocol)


      
def load_zipped_pickle(filename):
    with gzip.open(filename, 'rb') as f:
        loaded_object = cPickle.load(f)
        return loaded_object


# open the image
img = Image.open('me.jpg')
# convert the image into 3 arrays of R, G, B values
imgmats = get_RGB_matricies(img)

print imgmats

# run convert -delay 20 -loop 0 *.jpg svd.gif to make the gif
# scipy.misc.imsave('compressedMe.jpg', rgb)






