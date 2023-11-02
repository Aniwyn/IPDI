import skimage as skimage
import imageio.v2 as imageio
import numpy as np
import matplotlib.pyplot as plt
import src.PixelArithmetic as k

image = skimage.io.imread('../../resource/image1.png')
#image = imageio.imread('../../resource/image1.png')
print(image.shape[2])

plt.figure(1)
plt.subplot(211)
plt.imshow(image[:,:,0], cmap='gray')
plt.subplot(212)
plt.imshow(skimage.morphology.dilation(image[:,:,0], skimage.morphology.square(5)), cmap='gray')
plt.show()

aux1 = image.copy()
#for i in range(aux1.shape[2]):
#    aux1[:,:,i] = skimage.morphology.dilation(image[:,:,i], skimage.morphology.square(4))\
aux1[:,:,0] = skimage.morphology.dilation(image[:,:,0], skimage.morphology.square(4))
plt.imshow(aux1)
plt.show()

aux2 = image.copy()
aux2 = k.RGBtoYIQ_array(aux2)
aux2[:,:,0] = skimage.morphology.dilation(image[:,:,0], skimage.morphology.square(4))
aux2 = k.YIQtoRGB(aux2)
plt.imshow(aux1)
plt.show()